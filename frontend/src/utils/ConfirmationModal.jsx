import React from 'react'
import { Button, Center, Modal, Space, Text } from '@mantine/core'

function ConfirmationModal ({ opened, setOpened, title, body, func, buttonColor = 'red', buttonText = 'Yes' }) {
  return <Modal centered
        opened={opened}
        onClose={() => setOpened(false)}
        title={title}
        closeOnClickOutside={false}>
        <div>
          <Text>{body}</Text>
          <Space h="md" />
          <Center>
            <Button variant="filled"
                color={buttonColor}
                radius="md"
                size="sm"
                onClick={func}>
                {buttonText}
            </Button>
          </Center>
        </div>
    </Modal>
}

export default ConfirmationModal
