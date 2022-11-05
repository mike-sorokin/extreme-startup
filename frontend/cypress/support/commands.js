/* eslint-disable no-undef */
// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

import { mount } from 'cypress/react18'

Cypress.Commands.add('mount', mount)

// Creates a game from the home page
Cypress.Commands.add('createGame', (password) => {
  cy.contains('Create').click()
  cy.get('[data-cy="password-input"]').clear()
  cy.get('[data-cy="password-input"]').type(password)
  cy.get('form > .mantine-Button-root').click()
})

// Joins a game as a player from the home page
Cypress.Commands.add('joinGameAsPlayer', (gameId, name, url) => {
  cy.contains('Join').click()
  cy.get('[data-cy="game-id-input"]').clear()
  cy.get('[data-cy="game-id-input"]').type(gameId)
  cy.get('[data-cy="player-name-input"]').clear()
  cy.get('[data-cy="player-name-input"]').type(name)
  cy.get('[data-cy="url-input"]').clear()
  cy.get('[data-cy="url-input"]').type(url)
  cy.get('form > .mantine-UnstyledButton-root').click()
})

// Joins a game as a moderator from the home page
Cypress.Commands.add('joinGameAsModerator', (gameId, password) => {
  cy.contains('Join').click()
  cy.get('.mantine-8jlqcf').click()
  cy.get('[data-cy="mod-game-id-input"]').clear()
  cy.get('[data-cy="mod-game-id-input"]').type(gameId)
  cy.get('[data-cy="mod-pwd-input"]').clear()
  cy.get('[data-cy="mod-pwd-input"]').type(password)
  cy.get('form > .mantine-Button-root').click()
})
