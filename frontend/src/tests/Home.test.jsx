/* eslint-disable react/react-in-jsx-scope */
import { describe, expect, test } from 'vitest'
import { render, screen } from '@testing-library/react'
import { setup } from '@testing-library/user-event'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Home from '../components/Home'

const user = setup()

describe('Home', () => {
  test('clicking create game opens choose password dialog', async () => {
    render(<Home />)

    expect(screen.queryByRole('dialog', { name: 'Choose a password' })).toBeNull()

    await user.click(screen.getByRole('button', { name: 'Create a Game!' }))

    expect(screen.getByRole('dialog', { name: 'Choose a password' })).toBeInTheDocument()
  })

  test('submitting password creates game and displays game id', async () => {
    render(
      <BrowserRouter >
        <Routes>
          <Route path="*" element={<Home />} />
        </Routes>
      </BrowserRouter>
    )

    await user.click(screen.getByRole('button', { name: 'Create a Game!' }))

    await user.type(screen.getByLabelText(/Enter game password/i), 'test')

    await user.click(screen.getByRole('button', { name: 'Create Game!' }))

    expect(screen.queryByRole('dialog', { name: 'Choose a password' })).toBeNull()
    expect(screen.getByText('9bc9304c')).toBeInTheDocument()
  })
})
