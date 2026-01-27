export const fetchSubordinates = async (name, start_level = 1, end_level = 2) => {
  const params = new URLSearchParams({
    name: name,
    start_level: start_level.toString(),
    end_level: end_level.toString(),
  })
  //optimally this api endpoint is abstracted 
  const response = await fetch(`/view/subordinates?${params.toString()}`)
  console.log(response)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  return response.json()
}