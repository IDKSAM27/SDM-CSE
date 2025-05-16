function downloadResults(listId, filename) {
  const listItems = document.querySelectorAll(`#${listId} li`);
  const rows = Array.from(listItems).map(li => li.innerText);
  const blob = new Blob([rows.join('\n')], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}