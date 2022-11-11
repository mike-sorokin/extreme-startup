import React from 'react'
import { Button, Center, Modal, Space, Text } from '@mantine/core'

function ConfirmationModal ({ opened, setOpened, title, body, func }) {
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
                color="red"
                radius="md"
                size="sm"
                onClick={() => func}>
                Yes
            </Button>
          </Center>
        </div>
    </Modal>
}

export default ConfirmationModal
