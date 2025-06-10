'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import { fetchJson } from '@/lib/fetcher';

type Row = {
    time: string;
    buyInstantPrice: number;
    sellInstantPrice: number;
};

export function PriceChart({ product }: { product: string }) {
    const { data, isLoading, isError } = useQuery<Row[]>({
        queryKey: ['ticker', product],
        queryFn: () => fetchJson<Row[]>(`http://localhost:8000/api/product/${product}`),
        refetchInterval: 600_000, // 10 min
    });

    if (isLoading) return <p>Loading…</p>;
    if (isError || !data) return <p className="text-red-600">API error</p>;

    return (
        <Card>
            <CardHeader>
                <CardTitle>{product} — Buy vs Sell</CardTitle>
            </CardHeader>
            <CardContent className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="ds"
                            tickFormatter={(iso) => iso.slice(11, 16)} // HH:MM
                            minTickGap={20}
                        />
                        <YAxis />
                        <Tooltip />
                        <Line dataKey="inst_buyPrice" dot={false} strokeWidth={2} />
                        <Line dataKey="inst_sellPrices" dot={false} strokeDasharray="4 2" />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
