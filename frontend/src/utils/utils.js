import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';


export function str(obj) {
  return JSON.stringify(obj);
}

export function alertError(error) {
  console.log(error)
}

export function showSuccessfulNotification(msg) {
  showNotification({
    title: "Success",
    message: msg,
    icon: <IconCheck size={18} />,
    color: "teal"
  });
}
