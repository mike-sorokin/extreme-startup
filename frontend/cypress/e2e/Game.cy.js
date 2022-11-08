/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// Nav bar should be visible on all urls
// Nav bar buttons should navigate correctly
// Correct child components should be visible on their corresponding urls
// Check leaderboard and graph functionality here (requests, response, mock response, streaks, on fire, visible to everyone)

describe('Game page', () => {
  beforeEach(() => {
    cy.createGame('test')

    // save gameId of created game under alias gameId for tests to use later
    cy.get('[data-cy="game-id"]').invoke('text').as('gameId')
  })

  it('nav bar is visible on all game urls', function () {
    cy.visit('localhost:5173/' + this.gameId)
    cy.checkNavMenu()

    cy.visit('localhost:5173/' + this.gameId + '/players')
    cy.checkNavMenu()

    cy.visit('localhost:5173/' + this.gameId + '/admin')
    cy.checkNavMenu()

    cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')
    // waits up to 4s for player id to be visible before aliasing
    cy.get('[data-cy="player-id"]').should('be.visible')
    cy.get('[data-cy="player-id"]').invoke('text').as('playerId').then(() => {
      cy.visit('localhost:5173/' + this.gameId + '/players/' + this.playerId)
      cy.checkNavMenu()
    })
  })

  it('nav menu buttons should all work', function () {
    cy.visit('localhost:5173/' + this.gameId)

    cy.get('[data-cy="nav-menu"]').click()
    cy.contains('Host Page').click()
    cy.url().should('include', this.gameId + '/admin')
    cy.get('h1').should('have.text', 'Host Page')

    cy.get('[data-cy="nav-menu"]').click()
    cy.contains('Leaderboard').click()
    cy.url().should('include', this.gameId)
    cy.get('h1').should('have.text', 'Leaderboard')

    cy.get('[data-cy="nav-menu"]').click()
    cy.contains('Players').click()
    cy.url().should('include', this.gameId + '/players')
    cy.get('h1').should('have.text', 'Players')
  })

  it('sends requests for leaderboard', function () {
    // TODO check requests, response and mock response
  })
})
