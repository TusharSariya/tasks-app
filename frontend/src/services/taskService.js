export const fetchTasks = async () => {
    const response = await fetch('/view/tasks')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }