// import '@testing-library/jest-dom'
// import { render, screen } from '@testing-library/react'
import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'

// test('renders learn react link', () => {
//   expect(1+2).toEqual(3)
// })

it('renders without crashing', () => {
  const div = document.createElement('div')
  ReactDOM.render(<App />, div)
})
