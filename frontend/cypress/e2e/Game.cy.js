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
    cy.contains('Admin Page').click()
    cy.url().should('include', this.gameId + '/admin')
    cy.get('h1').should('have.text', 'Admin Page')

    cy.get('[data-cy="nav-menu"]').click()
    cy.contains('Leaderboard').click()
    cy.url().should('include', this.gameId)
    cy.get('h1').should('have.text', 'Leaderboard')

    cy.get('[data-cy="nav-menu"]').click()
    cy.contains('Players').click()
    cy.url().should('include', this.gameId + '/players')
    cy.get('h1').should('have.text', 'Players')
  })

  it('check requests for leaderboard', function () {
    cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')
    // waits up to 4s for player id to be visible before aliasing
    cy.get('[data-cy="player-id"]').should('be.visible')
    cy.get('[data-cy="player-id"]').invoke('text').as('playerId')

    cy.joinGameAsPlayer(this.gameId, 'jesse', 'https://www.google.co.uk')

    cy.visit('localhost:5173/' + this.gameId)

    cy.intercept('GET', '/api/' + this.gameId + '/players').as('fetch-players')

    cy.wait('@fetch-players').then(({ request, response }) => {
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.have.property('players')
      expect(Object.keys(response.body.players)).to.have.length(2)
      expect(response.body.players[this.playerId]).to.have.property('score')
    })

    cy.wait('@fetch-players').then(({ request, response }) => {
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.have.property('players')
      expect(Object.keys(response.body.players)).to.have.length(2)
      expect(response.body.players[this.playerId]).to.have.property('score')
    })
  })

  it('shows correct data on leaderboard for mock response data', function () {
    cy.intercept('GET', '/api/' + this.gameId + '/players', { fixture: 'players.json' })

    cy.visit('localhost:5173/' + this.gameId)

    // Assert that leaderboard table is sorted and displays information correctly
    cy.get('tbody > :nth-child(1) > :nth-child(2)').should('have.text', 'mock_jesse')

    cy.get('tbody > :nth-child(1) > :nth-child(1)').should('have.text', 'player2')
    cy.get('tbody > :nth-child(1) > :nth-child(4)').should('have.text', '420')
    cy.get('tbody > :nth-child(2) > :nth-child(1)').should('have.text', 'player3')
    cy.get('tbody > :nth-child(2) > :nth-child(4)').should('have.text', '21')
    cy.get('tbody > :nth-child(3) > :nth-child(1)').should('have.text', 'player1')
    cy.get('tbody > :nth-child(3) > :nth-child(4)').should('have.text', '-10')

    cy.get('tbody > :nth-child(2) > :nth-child(5)').should('have.text', ' ON FIRE! ')
    cy.get('tbody > :nth-child(1) > :nth-child(5)').should('have.text', '')

    // Annoying way to check that the streaks are of the correct colour
    cy.get('tbody > :nth-child(1) > :nth-child(3) > :nth-child(1) > :nth-child(1) > :nth-child(3)').should('have.css', 'background-color', 'rgb(255, 0, 0)')
    cy.get('tbody > :nth-child(1) > :nth-child(3) > :nth-child(1) > :nth-child(2) > :nth-child(3)').should('have.css', 'background-color', 'rgb(255, 165, 0)')
    cy.get('tbody > :nth-child(1) > :nth-child(3) > :nth-child(1) > :nth-child(3) > :nth-child(3)').should('have.css', 'background-color', 'rgb(0, 128, 0)')
  })

  it('shows correct graph for mock response data', function () {
    // TODO
  })
})
