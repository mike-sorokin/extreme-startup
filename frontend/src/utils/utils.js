export function str(obj) {
  return JSON.stringify(obj);
}

export function alertError(error) {
  console.log(error)
  // alert(str(error))
}
