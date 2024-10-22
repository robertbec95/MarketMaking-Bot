"use client"
import Transactions from "@/components/transactions"
import { useState, useEffect } from 'react'
import { DashboardData } from '@/types/api'
export default function Home() {
  const [data, setData] = useState<DashboardData | null>(null)
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/transactions')
      const result = await response.json()
      setData(result)
    }
    fetchData()
    const interval = setInterval(fetchData, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])
  if (!data) return <div>Loading...</div>
  console.log(data)
 
  return (
    <div>
      <Transactions />
      <h1>Market Making Dashboard</h1>
      <h2>Latest Balance</h2>
      <p>ETH: {data.latestBalance?.eth_balance}</p>
      <h2>Recent Transactions</h2>
      <ul>
        {data.recentTransactions.map((tx) => (
          <li key={tx.id}>{tx.type} - {tx.price} - {tx.amount} - {tx.timestamp}</li>
        ))}
      </ul>
    </div>
  )
}
