using UnityEngine;

public class SmoothCameraFollow : MonoBehaviour
{
    [SerializeField] private float damping; // How fast the camera will try to catch up to the target.
    public Transform target; // Making this public if we want to change the follow target.
    private Vector3 vel = Vector3.zero;

    [SerializeField] private float halfMapSize = 100f;
    private Camera mainCam;
    private float halfScreenHeight;
    private float halfScreenWidth;

    private void Awake()
    {
        mainCam = GetComponent<Camera>();

        // Visible area in world units
        halfScreenHeight = mainCam.orthographicSize;
        halfScreenWidth = halfScreenHeight * mainCam.aspect;
    }

    private void LateUpdate()
    {
        Vector3 targetPos = target.position;
        targetPos.z = gameObject.transform.position.z;

        targetPos.x = Mathf.Clamp(targetPos.x, -halfMapSize + halfScreenWidth, halfMapSize - halfScreenWidth);
        targetPos.y = Mathf.Clamp(targetPos.y, -halfMapSize + halfScreenHeight, halfMapSize - halfScreenHeight);

        // SmoothDamp gradually changes a vector towards a desired goal over time.
        gameObject.transform.position = Vector3.SmoothDamp(gameObject.transform.position, targetPos, ref vel, damping);
    }
}
