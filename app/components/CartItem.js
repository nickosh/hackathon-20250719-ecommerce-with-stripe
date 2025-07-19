import Image from "next/image"
import { useShoppingCart } from "use-shopping-cart"
import React from "react"

export default function CartItem({ item }) {
  const { name, emoji, quantity, price } = item
  const { removeItem, incrementItem, decrementItem } = useShoppingCart()

  const id = item.id || item.price_id // use the correct key!

  const handleRemove = () => {
    removeItem(id)
  }

  const handleAdd = () => {
    incrementItem(id, { count: 1 })
  }

  const handleSubtract = () => {
    if (quantity > 1) {
      decrementItem(id, { count: 1 })
    } else {
      removeItem(id)
    }
  }

  return (
    <div className="flex items-center gap-4 mb-3">
      <p className="text-4xl">{emoji}</p>
      <div>
        {name} <span className="text-xs">({quantity})</span>
      </div>
      <div className="ml-auto">￥{price * quantity}</div>

      <button
        onClick={handleAdd}
        className="bg-emerald-200 hover:bg-emerald-400 rounded w-8 h-8 flex items-center justify-center text-lg"
      >
        +
      </button>
      <button
        onClick={handleSubtract}
        className="bg-yellow-200 hover:bg-yellow-400 rounded w-8 h-8 flex items-center justify-center text-lg"
      >
        -
      </button>
      <button
        onClick={handleRemove}
        className="bg-red-200 hover:bg-red-400 rounded w-8 h-8 flex items-center justify-center"
      >
        <Image alt="delete icon" src="/trash.svg" width={16} height={16} />
      </button>
    </div>
  )
}
