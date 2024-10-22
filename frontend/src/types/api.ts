export interface Transaction {
    id: number;
    type: string;
    price: number;
    amount: number;
    timestamp: string;
  }
  
  export interface Balance {
    id: number;
    eth_balance: number;
    usd_balance: number;
    timestamp: string;
  }
  
  export interface DashboardData {
    recentTransactions: Transaction[];
    latestBalance: Balance;
  }