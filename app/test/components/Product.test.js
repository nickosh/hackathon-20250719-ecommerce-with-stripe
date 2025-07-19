import React from "react"
import { render, screen, fireEvent } from "@testing-library/react"
import Product from "../../components/Product"
import { formatCurrencyString } from "use-shopping-cart"

// Mock use-shopping-cart
const mockAddItem = jest.fn()

jest.mock("use-shopping-cart", () => ({
  useShoppingCart: () => ({
    addItem: mockAddItem,
  }),
  formatCurrencyString: jest.fn(),
}))

const mockProduct = {
  id: "prod_123",
  name: "Sushi",
  emoji: "🍣",
  price: 1000,
}

describe("Product component", () => {
  beforeEach(() => {
    jest.clearAllMocks()
    formatCurrencyString.mockImplementation(({ value, currency }) => {
      return `${currency} ${value / 100}` // Simple formatter
    })
  })

  it("renders product details correctly", () => {
    render(<Product product={mockProduct} />)

    expect(screen.getByText("🍣")).toBeInTheDocument()
    expect(screen.getByText("Sushi")).toBeInTheDocument()
    expect(screen.getByText("JPY 10")).toBeInTheDocument()
  })

  it("increments and decrements quantity", () => {
    render(<Product product={mockProduct} />)

    const incrementButton = screen.getByText("+")
    const decrementButton = screen.getByText("-")

    // Increase
    fireEvent.click(incrementButton)
    expect(screen.getByText("2")).toBeInTheDocument()

    // Decrease
    fireEvent.click(decrementButton)
    expect(screen.getByText("1")).toBeInTheDocument()

    // Should not go below 1
    fireEvent.click(decrementButton)
    expect(screen.getByText("1")).toBeInTheDocument()
  })

  it("calls addItem with correct count and resets quantity", () => {
    render(<Product product={mockProduct} />)

    const incrementButton = screen.getByText("+")
    const addToCartButton = screen.getByText("Add to cart")

    fireEvent.click(incrementButton)
    fireEvent.click(incrementButton)

    fireEvent.click(addToCartButton)

    expect(mockAddItem).toHaveBeenCalledWith(mockProduct, { count: 3 })

    expect(screen.getByText("1")).toBeInTheDocument()
  })
})
