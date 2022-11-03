/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

describe('Home page', () => {
  // Visit 'localhost:5173' and create a game with password before each test
  beforeEach(() => {
    cy.visit('localhost:5173')
    // Type a password and create a game
    cy.contains('Create').click()
    cy.get('[data-cy="password-input"]').clear()
    cy.get('[data-cy="password-input"]').type('test')
    cy.get('form > .mantine-Button-root').click()
  })

  it('creating game with pwd displays game id and success notification', () => {
    // Assert that a game id is visible
    cy.get('.mantine-1mwlxyv').should('be.visible')

    // Assert that a mantine notification is displayed with title 'Success'
    cy.get('.mantine-Notification-title').should('have.text', 'Success')
  })

  // using a function here so we can use aliases with this
  it('joining a game', function () {
    // Save gameId of created game
    cy.get('.mantine-1mwlxyv').invoke('text').as('gameId')
      .then(() => {
        // Go back to home page
        cy.visit('localhost:5173')

        // Enter details to join the newly created game
        cy.contains('Join').click()
        cy.get('[data-cy="game-id-input"]').clear()
        cy.get('[data-cy="game-id-input"]').type(this.gameId)
        cy.get('[data-cy="player-name-input"]').clear()
        cy.get('[data-cy="player-name-input"]').type('dev')
        cy.get('[data-cy="url-input"]').clear()
        cy.get('[data-cy="url-input"]').type('https://www.google.com')

        cy.get('form > .mantine-UnstyledButton-root').click()

        // Assert that player name and url is visible
        cy.contains('dev').should('be.visible')
        cy.contains('https://www.google.com').should('be.visible')

        // Assert that a mantine notification is displayed with title 'Success'
        cy.get('.mantine-Notification-title').should('have.text', 'Success')
      })
  })
})
