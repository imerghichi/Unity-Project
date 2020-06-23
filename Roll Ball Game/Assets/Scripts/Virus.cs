using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEngine.UI;

public class Virus : MonoBehaviour
{
    public Text countText;
    public Text winText;
    public Text countVies;

    private int nbreVies = 30;
    // Start is called before the first frame update
    void Start()
    {

    }

    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Joueur"))
        {

            nbreVies = nbreVies - 1;
            SetCountVies();


        }
    }
    void SetCountVies()
    {

        countVies.text = "Vies : " + nbreVies.ToString();
        if (nbreVies == 0)
        {
            winText.text = "Game Over";
            countText.text = "";
        }
    }
}