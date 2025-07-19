import handler from "../../pages/api/checkout"
import { createMocks } from "node-mocks-http"

jest.mock("stripe", () => {
  return jest.fn().mockImplementation(() => ({
    checkout: {
      sessions: {
        create: jest.fn().mockResolvedValue({
          id: "cs_test_sessionId",
        }),
      },
    },
  }))
})

describe("/api/checkout", () => {
  it("should return sessionId for valid cartDetails", async () => {
    const cartDetails = {
      price_123: {
        name: "Sushi",
        price: 120,
        quantity: 2,
        id: "price_123",
      },
    }

    const { req, res } = createMocks({
      method: "POST",
      body: { cartDetails },
    })

    await handler(req, res)

    expect(res._getStatusCode()).toBe(200)
    const json = JSON.parse(res._getData())
    expect(json.sessionId).toBe("cs_test_sessionId")
  })

  it("should return 405 for non-POST requests", async () => {
    const { req, res } = createMocks({
      method: "GET",
    })

    await handler(req, res)

    expect(res._getStatusCode()).toBe(405)
  })

  it("should return 400 for invalid cartDetails", async () => {
    const { req, res } = createMocks({
      method: "POST",
      body: {}, // no cartDetails
    })

    await handler(req, res)

    expect(res._getStatusCode()).toBe(400)
  })
})
