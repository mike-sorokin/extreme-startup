/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// approx time: 20s
// Test 1:
//  - Check all information is displayed correctly on initial render
// Test 2:
//  - Check fetchPlayer requests are being sent and check response format
// Test 3:
//  - Check all information (including events table) is displayed correctly from a mock response
//
// TODO: Check that only the player can see this page
// Player withdraw?
// Check events are correct based on round?

describe('Game page', () => {
  beforeEach(function () {
    cy.createGame('test')

    // save gameId of created game under alias gameId for tests to use later
    cy.get('[data-cy="game-id"]').invoke('text').as('gameId').then(() => {
      cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')
      // waits up to 4s for player id to be visible before aliasing
      cy.get('[data-cy="player-id"]').should('be.visible')
      cy.get('[data-cy="player-id"]').invoke('text').as('playerId')
    })
  })

  it('all information is displayed correctly on initial render', function () {
    cy.get('[data-cy="game-id"]').should('have.text', this.gameId)
    cy.get('[data-cy="api"]').should('have.text', 'https://www.google.com')
    cy.get('[data-cy="score"]').should('be.visible')
  })

  it('fetchPlayer requests are being sent and response has correct format', function () {
    cy.intercept('GET', '/api/' + this.gameId + '/players/' + this.playerId).as('fetch-player')

    cy.wait('@fetch-player').then(({ request, response }) => {
      console.log({ request, response })
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(JSON.parse(response.body)).to.have.property('name').and.to.equal('walter')
      expect(JSON.parse(response.body)).to.have.property('id').and.to.equal(this.playerId)
      expect(JSON.parse(response.body)).to.have.property('game_id').and.to.equal(this.gameId)
      expect(JSON.parse(response.body)).to.have.property('api').and.to.equal('https://www.google.com')
      expect(JSON.parse(response.body)).to.have.property('score')
      expect(JSON.parse(response.body)).to.have.property('events').and.to.be.an('array')
    })

    cy.wait('@fetch-player').then(({ request, response }) => {
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(JSON.parse(response.body)).to.have.property('name').and.to.equal('walter')
      expect(JSON.parse(response.body)).to.have.property('id').and.to.equal(this.playerId)
      expect(JSON.parse(response.body)).to.have.property('game_id').and.to.equal(this.gameId)
      expect(JSON.parse(response.body)).to.have.property('api').and.to.equal('https://www.google.com')
      expect(JSON.parse(response.body)).to.have.property('score')
      expect(JSON.parse(response.body)).to.have.property('events').and.to.be.an('array')
    })

    cy.wait('@fetch-player')
  })

  it('all information is displayed correctly from a mock response', function () {
    cy.intercept('GET', '/api/' + this.gameId + '/players/' + this.playerId, { fixture: 'player.json' }).as('fetch-player')
    cy.wait('@fetch-player')

    cy.get('h1').should('contain', 'mock_walter')
    cy.get('[data-cy="player-id"]').should('have.text', 'mock_id')
    cy.get('[data-cy="game-id"]').should('have.text', 'mock_game_id')
    cy.get('[data-cy="api"]').should('have.text', 'https://www.savewalterwhite.com')
    cy.get('[data-cy="score"]').should('have.text', '-420')

    // Check events table displays info correctly
    cy.get('tbody > :nth-child(1) > :nth-child(1)').should('have.text', 'mock_event_id_3')
    cy.get('tbody > :nth-child(1) > :nth-child(2)').should('have.text', 'What\'s up dog?')
    cy.get('tbody > :nth-child(1) > :nth-child(3)').should('have.text', '-1')
    cy.get('tbody > :nth-child(1) > :nth-child(4)').should('have.text', '0')
    cy.get('tbody > :nth-child(1) > :nth-child(5)').should('have.text', '5th June')
    cy.get('tbody > :nth-child(1) > :nth-child(6)').should('have.text', ' CORRECT ')
    cy.get('tbody > :nth-child(1) > :nth-child(6) > :nth-child(1)').should('have.css', 'background-color', 'rgba(47, 158, 68, 0.2)')

    cy.get('tbody > :nth-child(2) > :nth-child(1)').should('have.text', 'mock_event_id_2')
    cy.get('tbody > :nth-child(2) > :nth-child(2)').should('have.text', 'When did I ask?')
    cy.get('tbody > :nth-child(2) > :nth-child(3)').should('have.text', '0')
    cy.get('tbody > :nth-child(2) > :nth-child(4)').should('have.text', '-420')
    cy.get('tbody > :nth-child(2) > :nth-child(5)').should('have.text', 'time')
    cy.get('tbody > :nth-child(2) > :nth-child(6)').should('have.text', ' INCORRECT ')
    cy.get('tbody > :nth-child(2) > :nth-child(6) > :nth-child(1)').should('have.css', 'background-color', 'rgba(224, 49, 49, 0.2)')

    cy.get('tbody > :nth-child(3) > :nth-child(1)').should('have.text', 'mock_event_id_1')
    cy.get('tbody > :nth-child(3) > :nth-child(2)').should('have.text', 'Who was in paris?')
    cy.get('tbody > :nth-child(3) > :nth-child(3)').should('have.text', '21')
    cy.get('tbody > :nth-child(3) > :nth-child(4)').should('have.text', '420')
    cy.get('tbody > :nth-child(3) > :nth-child(5)').should('have.text', 'mock_timestamp')
    cy.get('tbody > :nth-child(3) > :nth-child(6)').should('have.text', ' NO RESPONSE ')
    cy.get('tbody > :nth-child(3) > :nth-child(6) > :nth-child(1)').should('have.css', 'background-color', 'rgba(240, 140, 0, 0.2)')
  })
})
