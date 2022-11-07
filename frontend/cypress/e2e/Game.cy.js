/* eslint-disable no-unused-expressions */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable no-undef */
/// <reference types="cypress" />

// Summary:
// Nav bar should be visible on all urls
// Nav bar buttons should work
// Maybe test styling on hover?
// Child components should be visible on correct urls
// Check leaderboard and graph functionality here (requests, response, mock response, streaks, on fire, visible to everyone)

describe('Game page', () => {
  beforeEach(() => {
    cy.createGame('test')
  })

  it('studio', () => {
    cy.get('[data-cy="to-game-page"]').click()
    cy.get('.mantine-Paper-root > :nth-child(2) > .mantine-Text-root').should('have.text', '484b2e3c')
    cy.get('[style="color: grey;"]').should('have.text', '0')
    cy.get('.mantine-Paper-root > :nth-child(1)').should('have.text', 'Game ID')
    cy.get('.mantine-Paper-root > :nth-child(5)').should('have.text', 'Number of Players')
    cy.get('.mantine-h9iq4m').should('have.text', 'WARMUP')
    cy.get('.mantine-140p204 > .mantine-3xbgk5 > .mantine-qo1k2').should('have.text', 'Advance Round')
    cy.get('.mantine-18wjb3e > .mantine-3xbgk5 > .mantine-qo1k2').should('have.text', 'Pause')
  })
})
