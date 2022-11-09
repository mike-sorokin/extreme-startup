/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// approx time: 34s
// Test 1:
//  - Check all information is displayed correctly on initial render
// Test 2:
//  - Check fetchAllPlayers requests are being sent and check response format
// Test 3:
//  - Player withdraw button works and player is removed from table
// Test 4:
//  - Withdraw all button works and players a removed from table
//
// TODO: Make sure players can only see their own withdraw button and cannot see the withdraw all button

describe('Game page', () => {
  beforeEach(function () {
    cy.createGame('test')

    // save gameId of created game under alias gameId for tests to use later
    cy.get('[data-cy="game-id"]').invoke('text').as('gameId').then(() => {
      cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')
      // waits up to 4s for player id to be visible before aliasing
      cy.get('[data-cy="player-id"]').should('be.visible')
      cy.get('[data-cy="player-id"]').invoke('text').as('playerId')
    }).then(() => {
      cy.joinGameAsPlayer(this.gameId, 'jesse', 'https://www.google.co.uk')
    })
  })

  it('all information is displayed correctly on initial render', function () {
    cy.visit('localhost:5173/' + this.gameId + '/players')

    // Check correct text is displayed
    cy.get('tbody > :nth-child(1) > :nth-child(2)').should('have.text', 'walter')
    cy.get('tbody > :nth-child(1) > :nth-child(3)').should('have.text', 'https://www.google.com')
    cy.get('tbody > :nth-child(2) > :nth-child(2)').should('have.text', 'jesse')
    cy.get('tbody > :nth-child(2) > :nth-child(3)').should('have.text', 'https://www.google.co.uk')

    // Check withdraw buttons are visible
    cy.get('tbody > :nth-child(1) > :nth-child(4)').should('have.text', 'Withdraw')
    cy.get('tbody > :nth-child(2) > :nth-child(4)').should('have.text', 'Withdraw')
    cy.contains('Withdraw All').should('be.visible')

    // Check that clicking on a player row takes you to that player page
    cy.get('tbody > :nth-child(1) > :nth-child(1)').click()
    cy.url().should('include', this.gameId + '/players/' + this.playerId)
    cy.get('h1').should('contain', 'walter')
  })

  it('fetchAllPlayers requests are being sent and response has correct format', function () {
    cy.visit('localhost:5173/' + this.gameId + '/players')

    cy.intercept('GET', '/api/' + this.gameId + '/players').as('fetch-players')

    cy.wait('@fetch-players').then(({ request, response }) => {
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.have.property('players')
      expect(Object.keys(response.body.players)).to.have.length(2)
      expect(response.body.players[this.playerId]).to.have.property('id').and.to.equal(this.playerId)
      expect(response.body.players[this.playerId]).to.have.property('name').and.to.equal('walter')
      expect(response.body.players[this.playerId]).to.have.property('api').and.to.equal('https://www.google.com')
    })

    cy.wait('@fetch-players').then(({ request, response }) => {
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.have.property('players')
      expect(Object.keys(response.body.players)).to.have.length(2)
      expect(response.body.players[this.playerId]).to.have.property('id')
      expect(response.body.players[this.playerId]).to.have.property('name')
      expect(response.body.players[this.playerId]).to.have.property('api')
    })

    cy.wait('@fetch-players')
  })

  it('player withdraw button works', function () {
    cy.visit('localhost:5173/' + this.gameId + '/players')

    cy.intercept('DELETE', '/api/' + this.gameId + '/players/' + this.playerId).as('withdraw-player')

    // Click withdraw button
    cy.get('tbody > :nth-child(1) > :nth-child(4) > .mantine-UnstyledButton-root').click()

    // Check request and response
    cy.wait('@withdraw-player').then(({ request, response }) => {
      console.log({ request, response })
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.deep.equal({ deleted: this.playerId })
    })

    // Check template
    cy.get('h1').should('have.text', 'Leaderboard')

    // Navigate back to players page and check player is removed
    cy.visit('localhost:5173/' + this.gameId + '/players')
    cy.contains('walter').should('not.exist')
  })

  it('withdraw all button works', function () {
    cy.visit('localhost:5173/' + this.gameId + '/players')

    cy.intercept('DELETE', '/api/' + this.gameId + '/players').as('withdraw-all-players')

    // Check that player shows in template
    cy.contains('walter').should('exist')

    // Click withdraw all button
    cy.get('[data-cy="withdraw-all"]').click()

    // Check request and response
    cy.wait('@withdraw-all-players').then(({ request, response }) => {
      console.log({ request, response })
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(204)
      expect(response.body).to.deep.equal('')
    })

    // Check that player is not shown in template
    cy.contains('walter').should('not.exist')
  })
})
