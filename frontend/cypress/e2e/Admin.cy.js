/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// Game ID, No. of players, current round, advance round button, pause round button should all be visible
// Check it sends requests to fetch game data and check responses are in the correct format
// Mock responses and check that it displays the data correctly (data = no. of players, current round, game paused)
// Check advance round button works
// Check pause game button works
// Maybe check questions stop being sent after pause? or new questions are sent after advance? (not sure how to do this)

describe('Game page', () => {
  beforeEach(() => {
    cy.createGame('test')
  })

  it('studio', () => {
  })
})
