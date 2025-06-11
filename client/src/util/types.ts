export type ApiResponse = {
    ds: string;
    inst_sellPrice: number;
    sellVolume: number;
    inst_sellPastWeek: number;
    sellOrders: number;
    inst_buyPrice: number;
    buyVolume: number;
    inst_buyPastWeek: number;
    buyOrders: number;
};
export type ProductKey = keyof ApiResponse;
export type KeyTuple = [keyof ApiResponse, keyof ApiResponse];
export type CorrelationData = Record<string, number>;
