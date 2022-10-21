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

export function showFailureNotification(header, msg) {
  showNotification({
    title: header,
    message: msg,
    icon: <IconX size={18} />,
    color: "red"
  });
}
