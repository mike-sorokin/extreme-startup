export function str(obj) {
  return JSON.stringify(obj);
}

export function alertError(error) {
  alert(str(error))
}
