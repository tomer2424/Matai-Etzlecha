using UnityEngine;

// Second weapon: frying pans that spin around the chef and hit whatever they touch.
public class PanWeapon : WeaponBase
{
    [SerializeField] private GameObject panPrefab;

    [SerializeField] private float radius = 1.8f;      // distance of the pans from the chef
    [SerializeField] private float spinSpeed = 180f;   // degrees per second

    protected override void Awake()
    {
        base.Awake();

        // Create one pan as a child of this weapon, and push it out to the radius
        GameObject pan = Instantiate(panPrefab, transform);
        pan.transform.localPosition = new Vector3(radius, 0f, 0f);
    }

    protected override void Update()
    {
        base.Update();   // keeps WeaponBase's attack timer running
        RotatePans();
    }

    // Spins the whole weapon around its own center, so its child pans orbit the chef
    private void RotatePans()
    {
        transform.Rotate(0f, 0f, spinSpeed * Time.deltaTime);
    }

    protected override bool TryAttack()
    {
        return false; // hitting comes in the next step
    }
}