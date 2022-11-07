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

    // save gameId of created game under alias gameId for tests to use later
    cy.get('.mantine-1mwlxyv').invoke('text').as('gameId')
  })

  it('can visit a valid game id', function () {
    cy.visit('localhost:5173/' + this.gameId)
    cy.contains('Leaderboard').should('be.visible')
    // cy.contains('Not Found').should('not.exist')
  })

  it('shows not found page when trying to visit a url with invalid game id', function () {
    cy.visit('localhost:5173/420')
    cy.contains('Not Found').should('be.visible')
  })

  it('only allows you to see your own player page', function () {
    // TODO (need to be able to check authentication of cookie with backend)
  })

  it('shows not found page when trying to visit a url with invalid player id', function () {
    cy.visit('localhost:5173/' + this.gameId + '/players/420')
    cy.contains('Not Found').should('be.visible')
  })

  it('shows not found page when visiting a url that does not exist', function () {
    cy.visit('localhost:5173/' + this.gameId + '/invalidurl')
    cy.contains('Not Found').should('be.visible')
  })
})
