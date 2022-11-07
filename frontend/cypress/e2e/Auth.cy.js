/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// You can only navigate to game id's that exist
// You can only navigate to your own player page
// You can only navigate to player pages for player id's that exist
// You can only see the link to the admin page if you are an admin
// You can only see the withdraw options for all players if you are an admin
// You can only see your individual withdraw option if your are a player (maybe it doesn't show at all and only shows on your player page)

describe('Game page', () => {
  beforeEach(() => {
    cy.createGame('test')
  })

  it('studio', () => {
  })
})
