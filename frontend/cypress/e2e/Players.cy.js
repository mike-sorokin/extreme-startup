/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// Check correct requests are sent and response correctly formatted
// Check list of players is displayed correctly (by mocking response)
// Check that withdrawing player/ all players works and they are removed from the table
// Maybe check auth here instead of Auth.cy

describe('Game page', () => {
  beforeEach(() => {
    cy.createGame('test')
  })

  it('studio', () => {
  })
})
