/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// Create game
//  - Creating a game with password should always work
//  - Should send a POST req to "/api" which should return new game object with id property
//  - Should be navigated to game admin page after clicking button
// Join game
//  - Joining a game should only work with valid game id, name and url
//  - Should send a POST req to "/api/(game_id)/players" which should return new player object
//  - Should be navigated to player page
// Join game as moderator
//  - Joining a game as moderator should only work with valid game id and correct password
//  - Should send a POST req to "/api/(gameId)/auth" which should return {valid: True} if pwd correct and {valid: False} if not
//  - Should be navigated to admin page

describe('Home page', () => {
  // Visit 'localhost:5173' and create a game with password before each test
  beforeEach(() => {
    cy.visit('localhost:5173')

    // Setup request intercept
    cy.intercept('POST', '/api').as('create-game')

    // Type a password and create a game
    cy.contains('Create').click()
    cy.get('[data-cy="password-input"]').clear()
    cy.get('[data-cy="password-input"]').type('test')
    cy.get('form > .mantine-Button-root').click()

    // Verify request was sent and returned response with status code 200
    // cy.wait('@create-game').its('response.statusCode').should('equal', 200)
    // cy.wait('@create-game').its('request.body').should('deep.equal', { password: 'test' })
    cy.wait('@create-game').then((interception) => {
      expect(interception.request.body).to.deep.equal({ password: 'test' })
      expect(interception.response.statusCode).to.equal(200)
      // Weirdly the response is not in JSON?
      expect(JSON.parse(interception.response.body)).to.have.property('id')
    })

    // save gameId of created game
    cy.get('.mantine-1mwlxyv').invoke('text').as('gameId')
  })

  it('creating game displays game id, success notification and navigates to correct url', function () {
    // Assert that a game id is visible
    cy.get('.mantine-1mwlxyv').should('be.visible')

    // Assert that a mantine notification is displayed with title 'Success'
    cy.get('.mantine-Notification-title').should('have.text', 'Success')

    // Click to go to game page
    cy.get('[data-cy="to-game-page"]').click()

    cy.url().should('include', this.gameId + '/admin')
  })

  // using a function here so we can use aliases with this
  it('joining a game', function () {
    // Go back to home page
    cy.visit('localhost:5173')

    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    // Enter details to join the newly created game
    cy.contains('Join').click()
    cy.get('[data-cy="game-id-input"]').clear()
    cy.get('[data-cy="game-id-input"]').type(this.gameId)
    cy.get('[data-cy="player-name-input"]').clear()
    cy.get('[data-cy="player-name-input"]').type('dev ')
    cy.get('[data-cy="url-input"]').clear()
    cy.get('[data-cy="url-input"]').type('https://www.google.com')
    cy.get('form > .mantine-UnstyledButton-root').click()

    // Assert that player name and url is visible
    cy.contains('dev').should('be.visible')
    cy.contains('https://www.google.com').should('be.visible')

    // Assert that a mantine notification is displayed with title 'Success'
    cy.get('.mantine-Notification-title').should('have.text', 'Success')

    // Assert that response contains all info we need
    cy.wait('@join-game').then((interception) => {
      expect(interception.request.body).to.deep.equal({ name: 'dev', api: 'https://www.google.com' })
      expect(interception.response.statusCode).to.equal(200)
      expect(interception.response.body).to.have.property('id')
      expect(interception.response.body).to.have.property('score')
      expect(interception.response.body.api).to.equal('https://www.google.com')
      expect(interception.response.body.name).to.equal('dev')
      expect(interception.response.body.game_id).to.equal(this.gameId)
    })

    cy.url().should('include', this.gameId + '/players')
  })

  it.only('join game as moderator', function () {
    // Go back to home page
    cy.visit('localhost:5173')

    cy.intercept('POST', '/api/' + this.gameId + '/auth').as('join-game-as-mod')

    // Join game as moderator
    cy.contains('Join').click()
    cy.get('.mantine-8jlqcf').click()
    cy.get('[data-cy="mod-game-id-input"]').clear()
    cy.get('[data-cy="mod-game-id-input"]').type(this.gameId)
    cy.get('[data-cy="mod-pwd-input"]').clear()
    // (Game password was given as test in the beforeEach hook)
    cy.get('[data-cy="mod-pwd-input"]').type('test')
    cy.get('form > .mantine-Button-root').click()
  })
})
