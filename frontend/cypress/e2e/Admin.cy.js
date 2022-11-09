/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// approx time: 16s
// Test 1:
//  - Game ID, No. of players, current round, advance round button, pause game button should all be visible
// Test 2 and 3:
//  - Check advance-round and pause-game buttons work
// Test 4:
//  - Check it sends fetchGame requests and check response ormat
// Test 5:
//  - Mock responses and check that it displays the data correctly (data = no. of players, current round)
//
// TODO: Check that this page is only visible to admins
// Maybe check questions stop being sent after pause? or new questions are sent after advance? (not sure how to do this)

describe('Game page', () => {
  beforeEach(function () {
    cy.createGame('test')

    // save gameId of created game under alias gameId for tests to use later
    cy.get('[data-cy="game-id"]').invoke('text').as('gameId').then(() => {
      // Navigate to game admin page and check we are on the correct url
      cy.get('[data-cy="to-game-page"]').click()
      cy.url().should('include', this.gameId + '/admin')
    })
  })

  it('check all info is displayed on the page', function () {
    // Check game id is visible
    cy.contains(this.gameId).should('be.visible')
    // Check number of players is zero initially
    cy.get('[data-cy="number-of-players"]').should('have.text', '0')
    // Check current round is set to WARMUP
    cy.get('[data-cy="current-round"]').should('have.text', 'WARMUP')
    // Check pause and advance round buttons are visible
    cy.get('[data-cy="advance-round-button"]').should('be.visible')
    cy.get('[data-cy="pause-game-button"]').should('be.visible')
  })

  it('advance round button works', function () {
    cy.get('[data-cy="current-round"]').should('have.text', 'WARMUP')

    // Setup request intercept
    cy.intercept('PUT', '/api/' + this.gameId).as('advance-round')

    // Click advance round button
    cy.get('[data-cy="advance-round-button"]').click()

    // Check request and response
    cy.wait('@advance-round').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ round: 1 })
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.equal('ROUND_INCREMENTED')
    })

    // Check template to see that round has updated
    cy.get('[data-cy="current-round"]').should('have.text', 'Round 1')

    // Click advance round again
    cy.get('[data-cy="advance-round-button"]').click()

    // Check request and response again
    cy.wait('@advance-round').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ round: 2 })
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.equal('ROUND_INCREMENTED')
    })

    // Check template again
    cy.get('[data-cy="current-round"]').should('have.text', 'Round 2')
  })

  it('pause game button works', function () {
    cy.get('[data-cy="current-round"]').should('have.text', 'WARMUP')
    cy.get('[data-cy="pause-game-button"]').should('have.text', 'Pause')

    // Setup request intercept
    cy.intercept('PUT', '/api/' + this.gameId).as('pause-game')

    // Click pause button
    cy.get('[data-cy="pause-game-button"]').click()

    // Check request and response
    cy.wait('@pause-game').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ pause: 'p' })
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.equal('GAME_PAUSED')
    })

    // Check template to see that paused is displayed
    cy.get('[data-cy="current-round"]').should('have.text', 'PAUSED')
    cy.get('[data-cy="pause-game-button"]').should('have.text', 'Resume')

    // Click resume button
    cy.get('[data-cy="pause-game-button"]').click()

    // Check request and response again
    cy.wait('@pause-game').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ pause: '' })
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.equal('GAME_UNPAUSED')
    })

    // Check template again
    cy.get('[data-cy="current-round"]').should('have.text', 'WARMUP')
    cy.get('[data-cy="pause-game-button"]').should('have.text', 'Pause')
  })

  it('check fetchGame requests are being sent and correct responses are received', function () {
    // Setup request intercept
    cy.intercept('GET', '/api/' + this.gameId).as('fetch-game')

    // Verify correct request and response
    cy.wait('@fetch-game').then(({ request, response }) => {
      console.log({ request, response })
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      // Response is not in JSON weirdly
      expect(JSON.parse(response.body)).to.have.property('id').and.to.equal(this.gameId)
      expect(JSON.parse(response.body)).to.have.property('round').and.to.equal(0)
      expect(JSON.parse(response.body)).to.have.property('players').and.to.deep.equal([])
      expect(JSON.parse(response.body)).to.have.property('paused').and.to.equal(false)
    })

    cy.wait('@fetch-game').then(({ request, response }) => {
      expect(request.body).to.equal('')
      expect(response.statusCode).to.equal(200)
      expect(JSON.parse(response.body)).to.have.property('id').and.to.equal(this.gameId)
      expect(JSON.parse(response.body)).to.have.property('round').and.to.equal(0)
      expect(JSON.parse(response.body)).to.have.property('players').and.to.deep.equal([])
      expect(JSON.parse(response.body)).to.have.property('paused').and.to.equal(false)
    })

    cy.wait('@fetch-game')
  })

  it('check correct data is displayed on the page from a mock response', function () {
    // Setup request intercept with mock response
    cy.intercept('GET', '/api/' + this.gameId, { fixture: 'new-game.json' }).as('fetch-game')
    cy.wait('@fetch-game')

    // Check correct data is displayed in template
    cy.contains(this.gameId).should('be.visible')
    cy.get('[data-cy="number-of-players"]').should('have.text', '3')
    cy.get('[data-cy="current-round"]').should('have.text', 'Round 15')
  })
})
