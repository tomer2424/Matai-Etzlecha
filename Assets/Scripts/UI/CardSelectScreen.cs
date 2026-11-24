using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class CardSelectScreen : MonoBehaviour
{
    [SerializeField] private GameObject cardsBackground;
    [SerializeField] private PlayerMovement playerMovement;
    private int pendingChoices = 0; // level ups that still wait for a card choice
    private int cardsToRoll;

    [SerializeField] private List<UpgradeOption> upgradeList;
    private UpgradeOption[] upgradesRolled = new UpgradeOption[3];

    [SerializeField] private TextMeshProUGUI[] cardsText;
    [SerializeField] private GameObject[] cards;

    private void HandleCards()
    {
        RollCards();
        ShowCardsText();
    }
    private void RollCards()
    {
        List<UpgradeOption> tempUpgradeList = new List<UpgradeOption>();
        foreach (UpgradeOption upgrade in upgradeList)
        {
            if (upgrade.IsAvailable())
            {
                tempUpgradeList.Add(upgrade);
            }
        }

        cardsToRoll = Mathf.Min(upgradesRolled.Length, tempUpgradeList.Count);

        for (int i = 0; i < cardsToRoll; i++)
        {
            int indexToPick = Random.Range(0, tempUpgradeList.Count);
            UpgradeOption tempUpgradeOption = tempUpgradeList[indexToPick];
            upgradesRolled[i] = tempUpgradeOption;
            tempUpgradeList.RemoveAt(indexToPick);
        }
    }

    private void ShowCardsText()
    {
        for (int i = 0; i < upgradesRolled.Length; i++)
        {
            if (i < cardsToRoll)
            {
                cards[i].SetActive(true);
                cardsText[i].text = upgradesRolled[i].Title + "\n" + upgradesRolled[i].Description;
            }
            else
            {
                cards[i].SetActive(false);
            }
            
        }
    }

    // Called by LevelSystem.OnLevelUp, once per level gained
    public void ShowCardScreen()
    {
        HandleCards();

        pendingChoices++;

        Time.timeScale = 0;
        cardsBackground.SetActive(true);
        playerMovement.enabled = false;
    }

    // Called by each card button
    public void OnCardButtonPress(int cardIndex)
    {
        upgradesRolled[cardIndex].Apply();
        pendingChoices--;

        // Close the screen only after every pending level up got its card
        if (pendingChoices == 0)
        {
            cardsBackground.SetActive(false);
            Time.timeScale = 1;
            playerMovement.enabled = true;
        }
        else
        {
            HandleCards();
        }
    }
}
