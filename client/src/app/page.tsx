'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ChartAreaInteractive } from '@/components/chart-area-interactive';
import { CorrelationBarChart } from '@/components/correlation-bar-chart';
import { useQuery, useQueries } from '@tanstack/react-query';
import { ApiResponse, CorrelationData } from '@/util/types';
import { Card, CardContent } from '@/components/ui/card';
import { X } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL!;

const fetchProduct = async (product: string): Promise<ApiResponse[]> => {
    const res = await fetch(`${API_URL}/api/product/${product}`);
    if (!res.ok) throw new Error('Failed to fetch product data');
    return res.json();
};

const fetchCorrelation = async (product: string): Promise<CorrelationData> => {
    const res = await fetch(`${API_URL}/api/correlation/${product}?prodKey=sellPrice&method=pearson`);
    if (!res.ok) throw new Error('Failed to fetch correlation data');
    return res.json();
};

export default function Dashboard() {
    const [input, setInput] = useState('');
    const [products, setProducts] = useState<string[]>(['ENCHANTED_DIAMOND']);

    const addProduct = () => {
        const trimmed = input.trim().toUpperCase();
        if (trimmed && !products.includes(trimmed)) {
            setProducts([...products, trimmed]);
        }
        setInput('');
    };

    const removeProduct = (product: string) => {
        setProducts((prev) => prev.filter((p) => p !== product));
    };

    const productQueries = useQueries({
        queries: products.map((product) => ({
            queryKey: ['product', product],
            queryFn: () => fetchProduct(product),
            refetchInterval: 600_000,
        })),
    });

    return (
        <main className="p-6 space-y-6">
            <div className="flex gap-2">
                <Input
                    placeholder="Enter product key…"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && addProduct()}
                />
                <Button onClick={addProduct}>Add</Button>
            </div>

            {productQueries.map((query, index) => {
                const product = products[index];
                const { data, isLoading, isError } = query;
                const {
                    data: correlationData,
                    isLoading: corrLoading,
                    isError: corrError,
                } = useQuery({
                    queryKey: ['correlation', product],
                    queryFn: () => fetchCorrelation(product),
                });

                return (
                    <Card key={product}>
                        <CardContent className="pt-4">
                            <div className="flex justify-between items-center mb-2">
                                <h3 className="text-lg font-semibold">{product}</h3>
                                <Button
                                    size="icon"
                                    variant="ghost"
                                    onClick={() => removeProduct(product)}
                                    className="text-muted-foreground"
                                >
                                    <X className="w-4 h-4" />
                                </Button>
                            </div>
                            {isLoading && <p>Loading…</p>}
                            {isError && <p className="text-red-600">Error loading data</p>}
                            {data && (
                                <>
                                    <ChartAreaInteractive
                                        productData={data}
                                        productKeys={['inst_buyPrice', 'inst_sellPrice']}
                                    />
                                    <ChartAreaInteractive
                                        productData={data}
                                        productKeys={['inst_buyPastWeek', 'inst_sellPastWeek']}
                                    />
                                    <ChartAreaInteractive
                                        productData={data}
                                        productKeys={['sellVolume', 'buyVolume']}
                                    />
                                    {correlationData && (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-6">
                                            <CorrelationBarChart correlationData={correlationData} />
                                            <CorrelationBarChart correlationData={correlationData} />
                                        </div>
                                    )}
                                </>
                            )}
                        </CardContent>
                    </Card>
                );
            })}
        </main>
    );
}
