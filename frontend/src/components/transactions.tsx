"use client"
import { useState, useEffect } from 'react'
import { DashboardData, Transaction } from '@/types/api'
import { Skeleton } from "@/components/ui/skeleton"
import Image from "next/image"
import { Badge } from './ui/badge'

export default function Transactions() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/transactions')
        const result = await response.json()
        setData(result)
        setIsLoading(false)
      } catch (err) {
        setError(err instanceof Error ? err : new Error('An error occurred'))
        setIsLoading(false)
      }
    }
    fetchData()
    const interval = setInterval(fetchData, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const formatDate = (date: string) => {
    const dateObj = new Date(date);
    return dateObj.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (error) {
    return <div className='flex justify-center items-center h-screen'>Error loading transactions: {error.message}</div>;
  }

  return (
    <div className='w-full'>
      <div className="mx-auto max-w-6xl px-2 sm:px-6">
        <div className="flex flex-col gap-2 mb-5">
          <h3 className="text-2xl">Last transactions</h3>
          <h4 className="text-sm font-thin">
            Transactions are updated every 5 seconds (Most recent first)
          </h4>
           <div className='bg-white text-black p-3 rounded-lg flex justify-between items-center gap-2 mt-4'>
            <h2 className="text-xl font-semibold">Latest Balance</h2>
            <Badge variant="outline" className="bg-blue-500 text-white">
              {data?.latestBalance?.eth_balance.toFixed(2)} ETH
            </Badge>
            <Badge variant="outline" className="bg-green-500 text-white">
              {data?.latestBalance?.usd_balance.toFixed(2)} USD
            </Badge>
           </div>

        </div>
          {isLoading ? (
            <Skeleton className="w-full h-40" />
          ) : data && data.recentTransactions.length > 0 ? (
            <div className="grid grid-cols-1 gap-4">
              {data.recentTransactions.map((transaction: Transaction) => (
                <div key={transaction.id} className="bg-gray-100 rounded-md p-4 text-black">
                  <div className="grid gap-2 lg:grid-cols-5 items-center">
                    <div className="flex items-center">
                      <Image src="/eth.svg" alt="Bitcoin" className="w-4 h-4 mr-2" width={16} height={16} />
                      <div className="text-lg text-orange-400">ETH/USD</div>
                    </div>
                    <div className="text-lg font-semibold flex items-center space-x-2">
                      <Badge 
                        variant="outline"
                        className={transaction.type === "PLACE_ASK" ? "bg-green-500 text-white" : "bg-red-500 text-white"}
                      >
                        {transaction.type}
                      </Badge>
                    </div>
                    <div className="text-md">Amount: {transaction.amount} </div>
                    <div className="text-md">Price: ${transaction.price.toFixed(2)}</div>
                    <div className="col-span-2 sm:col-span-3 lg:col-span-1 text-sm">
                      {formatDate(transaction.timestamp)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div>No transactions available</div>
          )}
        </div>
       
      </div>
  )
}