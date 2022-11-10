/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// approx time: 38s
// Create game
//  - Creating a game with password should always work unless you enter an empty password
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
//
// TODO: check cookies coming from server response

describe('Home page', () => {
  // Visit 'localhost:5173' and create a game with password before each test
  beforeEach(() => {
    // Setup request intercept
    cy.intercept('POST', '/api').as('create-game')

    cy.createGame('test')

    // Verify request was sent and returned response with status code 200
    cy.wait('@create-game').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ password: 'test' })
      expect(response.statusCode).to.equal(200)
      // Weirdly the response is not in JSON?
      expect(JSON.parse(response.body)).to.have.property('id')
    })

    // save gameId of created game under alias gameId for tests to use later
    cy.get('[data-cy="game-id"]').invoke('text').as('gameId')
  })

  // must use a function so we can use aliases with this
  it('creating game displays game id, success notification and navigates to correct url', function () {
    // Assert that a game id is visible
    cy.get('[data-cy="game-id"]').should('be.visible')

    // Assert success notification is shown
    cy.contains('Successfully Created Game').should('be.visible')

    // Click to go to game page
    cy.get('[data-cy="to-game-page"]').click()

    cy.url().should('include', this.gameId + '/admin')
  })

  it.only('does not allow you to give an empty password', function () {
    // Setup request intercept
    cy.intercept('POST', '/api').as('create-game-empty-pwd')

    // Try to create a game with empty password
    cy.visit('localhost:5173')
    cy.contains('Create').click()
    cy.get('[data-cy="password-input"]').clear()
    cy.get('[data-cy="password-input"]').type(' ')
    cy.get('form > .mantine-Button-root').click()

    // Assert error is shown
    cy.contains('password cannot be empty').should('be.visible')

    // Assert create-game request was not sent
    cy.get('@create-game-empty-pwd').should('equal', null)

    cy.url().should('equal', 'http://localhost:5173/')
  })

  it('joining a game', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    cy.joinGameAsPlayer(this.gameId, 'walter ', 'https://www.google.com')

    // Assert that player name and url is visible
    cy.contains('walter').should('be.visible')
    cy.contains('https://www.google.com').should('be.visible')

    cy.contains('Successfully Created Player').should('be.visible')

    // Assert that response contains all info we need
    cy.wait('@join-game').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ name: 'walter', api: 'https://www.google.com' })
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.have.property('id')
      expect(response.body).to.have.property('score')
      expect(response.body.api).to.equal('https://www.google.com')
      expect(response.body.name).to.equal('walter')
      expect(response.body.game_id).to.equal(this.gameId)
    })

    cy.url().should('include', this.gameId + '/players')
  })

  it('joining a game with invalid game id', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    cy.joinGameAsPlayer('invalid-id', 'walter ', 'https://www.google.com')

    // Assert error is shown
    cy.contains('Game id does not exist').should('be.visible')

    // Assert join-game request was not sent
    cy.get('@join-game').should('equal', null)

    cy.url().should('not.include', this.gameId + '/players')
  })

  it('joining a game with invalid url', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    cy.joinGameAsPlayer(this.gameId, 'walter', 'www.google.com')

    // Assert error is shown
    cy.contains('invalid URL').should('be.visible')

    // Assert join-game request was not sent
    cy.get('@join-game').should('equal', null)

    cy.url().should('not.include', this.gameId + '/players')
  })

  it('joining a game with empty name', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    cy.joinGameAsPlayer(this.gameId, ' ', 'https://www.google.com')

    // Assert error is shown
    cy.contains('Your name cannot be empty').should('be.visible')

    // Assert join-game request was not sent
    cy.get('@join-game').should('equal', null)

    cy.url().should('not.include', this.gameId + '/players')
  })

  it('joining a game with non-unique name', function () {
    // Join game with name 'walter'
    cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')

    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    // Try and join with same name
    cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')

    // Assert error is shown
    cy.contains('Your name already exists').should('be.visible')

    // Assert join-game request was not sent
    cy.get('@join-game').should('equal', null)

    cy.url().should('not.include', this.gameId + '/players')
  })

  it('joining a game with non-unique url', function () {
    // Join game with a url
    cy.joinGameAsPlayer(this.gameId, 'walter', 'https://www.google.com')

    cy.intercept('POST', '/api/' + this.gameId + '/players').as('join-game')

    // Try and join with the same url
    cy.joinGameAsPlayer(this.gameId, 'jesse', 'https://www.google.com')

    // Assert error is shown
    cy.contains('Your url already exists').should('be.visible')

    // Assert join-game request was not sent
    cy.get('@join-game').should('equal', null)

    cy.url().should('not.include', this.gameId + '/players')
  })

  it('joining a game as moderator', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/auth').as('join-game-as-mod')

    cy.joinGameAsModerator(this.gameId, 'test')

    // Assert correct request/response was sent/received
    cy.wait('@join-game-as-mod').then(({ request, response }) => {
      expect(request.body).to.deep.equal({ password: 'test' })
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.deep.equal({ valid: true })
    })

    cy.url().should('include', this.gameId + '/admin')
  })

  it('joining a game as moderator with invalid game id', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/auth').as('join-game-as-mod')

    cy.joinGameAsModerator('invalid-id', 'test')

    // Assert error is shown
    cy.contains('Game id does not exist').should('be.visible')

    // Assert join-game request was not sent
    cy.get('@join-game-as-mod').should('equal', null)

    cy.url().should('not.include', this.gameId + '/admin')
  })

  it('joining a game as moderator with incorrect password', function () {
    cy.intercept('POST', '/api/' + this.gameId + '/auth').as('join-game-as-mod')

    cy.joinGameAsModerator(this.gameId, 'incorrect-password')

    // Assert correct request/response was sent/received
    cy.wait('@join-game-as-mod').then(({ request, response }) => {
      expect(response.statusCode).to.equal(200)
      expect(response.body).to.deep.equal({ valid: false })
    })

    cy.url().should('not.include', this.gameId + '/admin')
  })
})
