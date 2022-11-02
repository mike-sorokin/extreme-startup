/* eslint-disable no-undef */
import matchers from '@testing-library/jest-dom/matchers'
import { expect, afterAll, afterEach, beforeAll } from 'vitest'
import { setupServer } from 'msw/node'
import { rest } from 'msw'

expect.extend(matchers)

// Need to mock the window.matchMedia property for some reason
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
})

// Mock backend and intercept requests (may need to move this to individual test files as it interferes with testing requests)
const games = {
  '9bc9304c': { id: '9bc9304c', round: 0, players: [], paused: false }
}

export const restHandlers = [
  rest.get('http://localhost:5000/api', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json(games))
  }),
  rest.post('http://localhost:5000/api', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json(games['9bc9304c']))
  })
]

const server = setupServer(...restHandlers)

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))

//  Close server after all tests
afterAll(() => server.close())

// Reset handlers after each test `important for test isolation`
afterEach(() => server.resetHandlers())
