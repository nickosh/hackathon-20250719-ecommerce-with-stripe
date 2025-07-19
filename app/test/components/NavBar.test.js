jest.mock("next/image", () => ({
  __esModule: true,
  default: (props) => {
    return <img {...props} />
  },
}))

jest.mock("next/link", () => ({
  __esModule: true,
  default: ({ children, href }) => <a href={href}>{children}</a>,
}))

const mockHandleCartClick = jest.fn()
jest.mock("use-shopping-cart", () => ({
  useShoppingCart: () => ({
    handleCartClick: mockHandleCartClick,
    cartCount: 3,
  }),
}))

import React from "react"
import { render, screen, fireEvent } from "@testing-library/react"
import NavBar from "../../components/NavBar"

describe("NavBar", () => {
  it("renders brand title and cart count", () => {
    render(<NavBar />)

    // Brand title
    expect(screen.getByText("QA Hacktahon")).toBeInTheDocument()

    // Cart count
    expect(screen.getByText("3")).toBeInTheDocument()

    // Cart icon (rendered as <img> in test)
    expect(screen.getByRole("img")).toHaveAttribute("alt", "shopping cart icon")
  })

  it("calls handleCartClick when cart icon is clicked", () => {
    render(<NavBar />)

    const buttons = screen.getAllByRole("button")
    fireEvent.click(buttons[0]) // index 0 is the cart button

    expect(mockHandleCartClick).toHaveBeenCalled()
  })
})
