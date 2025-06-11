'use client';

import * as React from 'react';
import { Area, AreaChart, CartesianGrid, XAxis } from 'recharts';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
    ChartConfig,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
} from '@/components/ui/chart';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ApiResponse, KeyTuple } from '@/util/types';
import { LineChart, Line, YAxis } from 'recharts';
export const description = '';

//const chartData = [
//{ date: '2024-04-01', desktop: 222, mobile: 150 },
//{ date: '2024-04-02', desktop: 97, mobile: 180 },

const chartConfig = {
    price: {
        label: 'Price',
    },
    buyPrice: {
        label: 'Key A',
        color: 'var(--chart-2)',
    },
    sellPrice: {
        label: 'Key aÀ',
        color: 'var(--chart-2)',
    },
} satisfies ChartConfig;

export function ChartAreaInteractive({
    productData,
    productKeys,
}: {
    productData: ApiResponse[];
    productKeys: KeyTuple;
}) {
    const [timeRange, setTimeRange] = React.useState('90d');
    const [keyA, keyB] = productKeys;

    const dynamicChartConfig: ChartConfig = {
        price: {
            label: 'Price',
        },
        a: {
            label: keyA,
            color: 'var(--chart-1)',
        },
        b: {
            label: keyB,
            color: 'var(--chart-2)',
        },
    } satisfies ChartConfig;

    const chartData = productData.map((item) => ({
        date: item.ds,
        a: item[keyA],
        b: item[keyB],
    }));
    const filteredData = chartData.filter((item) => {
        const date = new Date(item.date);
        const referenceDate = new Date('2024-06-30');
        let daysToSubtract = 90;
        if (timeRange === '30d') {
            daysToSubtract = 30;
        } else if (timeRange === '7d') {
            daysToSubtract = 7;
        }
        const startDate = new Date(referenceDate);
        startDate.setDate(startDate.getDate() - daysToSubtract);
        return date >= startDate;
    });

    return (
        <Card className="pt-0 border-none shadow-none rounded-none">
            <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>
                        "{productKeys[0]}" vs. "{productKeys[0]}"
                    </CardTitle>
                    <CardDescription className="hidden"></CardDescription>
                </div>
                <Select value={timeRange} onValueChange={setTimeRange}>
                    <SelectTrigger
                        //className="hidden w-[160px] rounded-lg sm:ml-auto sm:flex"
                        className="hidden w-[160px] rounded-lg sm:ml-auto"
                        aria-label="Select a value"
                    >
                        <SelectValue placeholder="Last 3 months" />
                    </SelectTrigger>
                    <SelectContent className="rounded-xl">
                        <SelectItem value="90d" className="rounded-lg">
                            Last 3 months
                        </SelectItem>
                        <SelectItem value="30d" className="rounded-lg">
                            Last 30 days
                        </SelectItem>
                        <SelectItem value="7d" className="rounded-lg">
                            Last 7 days
                        </SelectItem>
                    </SelectContent>
                </Select>
            </CardHeader>
            <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
                <ChartContainer config={dynamicChartConfig} className="aspect-auto h-[250px] w-full">
                    <LineChart data={filteredData}>
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="date"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            minTickGap={32}
                            tickFormatter={(value) => {
                                const date = new Date(value);
                                return date.toLocaleDateString('en-US', {
                                    month: 'short',
                                    day: 'numeric',
                                });
                            }}
                        />
                        <YAxis domain={['dataMin - 10', 'dataMax + 10']} />
                        <ChartTooltip
                            cursor={false}
                            content={
                                <ChartTooltipContent
                                    labelFormatter={(value) => {
                                        return new Date(value).toLocaleDateString('en-US', {
                                            month: 'short',
                                            day: 'numeric',
                                        });
                                    }}
                                    indicator="dot"
                                />
                            }
                        />
                        <Line
                            dataKey="a"
                            type="monotone"
                            stroke={chartConfig.sellPrice.color}
                            strokeWidth={2}
                            dot={false}
                        />
                        <Line
                            dataKey="b"
                            type="monotone"
                            stroke={chartConfig.buyPrice.color}
                            strokeWidth={2}
                            strokeDasharray="4 2"
                            dot={false}
                        />
                        <ChartLegend content={<ChartLegendContent />} />
                    </LineChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}
