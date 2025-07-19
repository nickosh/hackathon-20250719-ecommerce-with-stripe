import React from "react"

export default function Cancel() {
  return (
    <div className="text-center p-8">
      <h1 style={{ color: "red" }}>❌ Payment was canceled.</h1>
      <a
        href="/"
        className="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
      >
        Return to Home
      </a>
    </div>
  )
}
