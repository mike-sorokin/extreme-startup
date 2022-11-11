import React from 'react'
import ReactDOM from 'react-dom/client'
import { MantineProvider } from '@mantine/core'
import { NotificationsProvider } from '@mantine/notifications'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <MantineProvider theme={{ colorScheme: 'dark' }} withGlobalStyles withNormalizeCSS>
    <NotificationsProvider position='top-right' limit={1}>
      <App />
    </NotificationsProvider>
  </MantineProvider>
)
