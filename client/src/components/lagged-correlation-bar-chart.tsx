'use client';

import { Bar, BarChart, CartesianGrid, Cell, LabelList, XAxis, YAxis, ReferenceLine } from 'recharts';
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart';
import { Input } from '@/components/ui/input';
import { CorrelationData } from '@/util/types';
import { useQuery, useQueries } from '@tanstack/react-query';

export const description = '';
const TIME_STEP = Number(process.env.NEXT_PUBLIC_TIME_STEP!) || 10; //timestep in the current dataset is 10 minutes, eventhough its fetched every 5
const API_URL = process.env.NEXT_PUBLIC_API_URL!;

const fetchLaggedCorrelation = async (product: string, lag: number): Promise<CorrelationData> => {
    let tempLag = Math.ceil((lag * 60) / TIME_STEP);
    const res = await fetch(`${API_URL}/api/lagged_correlation/${product}?metric=sellPrice&lagSteps=${tempLag}`);
    if (!res.ok) throw new Error('Failed to fetch lagged correlation data');
    return res.json();
};

const chartConfig = {
    correlation: {
        label: 'correlation',
    },
} satisfies ChartConfig;

export function LaggedCorrelationBarChart({ productId, defaultLag = 0 }: { productId: string; defaultLag?: number }) {
    const [lag, setLag] = useState(defaultLag);

    const {
        data: correlationData,
        isLoading,
        isError,
    } = useQuery({
        queryKey: ['laggedCorrelation', productId, lag],
        queryFn: () => fetchLaggedCorrelation(productId, lag),
        //keepPreviousData: true,
    });

    let content = null;

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(e.target.value);
        setLag(isNaN(val) ? 0 : val);
    };

    if (isLoading) {
        content = <div>Loading lagged correlation…</div>;
    } else if (isError || !correlationData) {
        content = <div className="text-red-600">Error loading lagged correlation data</div>;
    } else {
        const chartData = Object.entries(correlationData)
            .map(([prodId, value]) => ({
                product: prodId,
                correlation: value,
            }))
            .sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation));

        content = (
            <ChartContainer config={chartConfig}>
                <BarChart accessibilityLayer data={chartData}>
                    <CartesianGrid vertical={false} />
                    <ChartTooltip
                        cursor={false}
                        content={<ChartTooltipContent hideIndicator labelFormatter={(label) => label} />}
                    />
                    <YAxis
                        domain={[-1, 1.04]} //TODO: same as the other one in correlation bar chart, change this to be -1, 1 but also make sure the 1 is visible
                        ticks={[1, 0.5, 0, -0.5, -1]}
                        axisLine={false}
                        tickLine={false}
                        allowDataOverflow={true}
                        type="number"
                    />
                    <XAxis dataKey="product" tick={false} axisLine={false} />
                    <ReferenceLine y={0} stroke="#575656" strokeWidth={1} />
                    <Bar dataKey="correlation" radius={[2, 2, 0, 0]}>
                        {chartData.map((item) => (
                            <Cell
                                key={item.product}
                                fill={item.correlation > 0 ? 'var(--chart-2)' : 'var(--chart-1)'}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ChartContainer>
        );
    }

    return (
        <Card className="pt-0 border-none shadow-none rounded-none">
            <CardHeader className="flex flex-row items-center justify-between">
                <div>
                    <CardTitle>Lagged Correlation</CardTitle>
                    <CardDescription>Top 5 strongest lagged Pearson Correlation</CardDescription>
                </div>
                <Input
                    className="w-24 ml-4"
                    type="number"
                    min={0}
                    step={0.5}
                    value={lag}
                    onChange={handleInputChange}
                    placeholder="Lag (h)"
                />
            </CardHeader>
            <CardContent>{content}</CardContent>
            <CardFooter className="flex-col items-start gap-2 text-sm">
                <div className="text-muted-foreground leading-none">
                    A high correlaton indicates that it correlates to what {productId} does {lag * TIME_STEP}min in the
                    future
                </div>
            </CardFooter>
        </Card>
    );
}
