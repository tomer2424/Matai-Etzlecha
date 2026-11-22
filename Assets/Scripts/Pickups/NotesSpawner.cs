using UnityEngine;
using UnityEngine.Pool;

public class NotesSpawner : MonoBehaviour
{
    [SerializeField] private NoteBehaviour notePrefab;
    private ObjectPool<NoteBehaviour> notesPool;


    private void Awake()
    {
        notesPool = new ObjectPool<NoteBehaviour>(CreateNewNote, OnNoteTaken, OnNoteReturned, DestroyNote);
    }

    private NoteBehaviour CreateNewNote()
    {
        NoteBehaviour note = Instantiate(notePrefab, gameObject.transform);
        note.SetPool(notesPool);
        return note;
    }
    private void OnNoteTaken(NoteBehaviour note)
    {
        note.gameObject.SetActive(true);
    }
    private void OnNoteReturned(NoteBehaviour note)
    {
        note.gameObject.SetActive(false);
    }
    private void DestroyNote(NoteBehaviour note)
    {
        if (note != null)
        {
            Destroy(note.gameObject);
        }
    }

    public void SpawnNote(Vector2 spawnPosition, int xpAmount)
    {
        NoteBehaviour note = notesPool.Get();
        note.SetXPAmount(xpAmount);
        note.transform.position = spawnPosition;
    }
}
