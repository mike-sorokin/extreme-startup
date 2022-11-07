/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// Maybe check auth here instead of Auth.cy (check only players can see their own player page)
// Check correct requests and response formatting
// Mock response and check data is displayed correctly
// Player withdraw?
// Update functionality?
// Check events are correct based on round?

describe('Game page', () => {
  beforeEach(() => {
    cy.createGame('test')
  })

  it('studio', () => {
  })
})
