using UnityEngine;

public class SmoothCameraFollow : MonoBehaviour
{
    [SerializeField] private float damping; // How fast the camera will try to catch up to the target.

    public Transform target; // Making this public if we want to change the follow target.
    private Vector3 vel = Vector3.zero;

    private void LateUpdate()
    {
        Vector3 targetPos = target.position;
        targetPos.z = gameObject.transform.position.z;

        // SmoothDamp gradually changes a vector towards a desired goal over time.
        gameObject.transform.position = Vector3.SmoothDamp(gameObject.transform.position, targetPos, ref vel, damping);
    }
}
