'use client';

import { TrendingUp } from 'lucide-react';
import { Bar, BarChart, CartesianGrid, Cell, LabelList, XAxis, YAxis, ReferenceLine } from 'recharts';

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart';
import { CorrelationData } from '@/util/types';

export const description = 'A bar chart with negative values';

const chartConfig = {
    correlation: {
        label: 'correlation',
    },
} satisfies ChartConfig;

export function CorrelationBarChart({ correlationData }: { correlationData: CorrelationData }) {
    const chartData = Object.entries(correlationData)
        .map(([prodId, value]) => ({
            product: prodId,
            correlation: value,
        }))
        .sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation));

    return (
        <Card>
            <CardHeader>
                <CardTitle>1:1 Correlation</CardTitle>
                <CardDescription>Top 5 stronges Pearson Correlation</CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig}>
                    <BarChart accessibilityLayer data={chartData}>
                        <CartesianGrid vertical={false} />
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent hideIndicator labelFormatter={(label) => label} />}
                        />
                        <YAxis
                            domain={[-1, 1]}
                            ticks={[1, 0.5, 0, -0.5, -1]}
                            axisLine={false}
                            tickLine={false}
                            allowDataOverflow={true}
                        />
                        <XAxis dataKey="product" tick={false} axisLine={false} />
                        <ReferenceLine y={0} stroke="#ccc" strokeWidth={1} />
                        <Bar dataKey="correlation">
                            {chartData.map((item) => (
                                <Cell
                                    key={item.product}
                                    fill={item.correlation > 0 ? 'var(--chart-2)' : 'var(--chart-1)'}
                                />
                            ))}
                        </Bar>
                    </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}
