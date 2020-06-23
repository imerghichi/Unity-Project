using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class ControleurJoueur : MonoBehaviour
{
    public float speed;
    public Text countText;
    public Text winText;
    public Text countVies;

    

    private Rigidbody rb;
    private int count;
    private int nbreVies = 10;

    void Start()
    {

        rb = GetComponent<Rigidbody>();
        count = 0;
        SetCountText();
        SetCountVies();
        winText.text = "";
    }
  
    void FixedUpdate()
    {
        float moveHorizontal = Input.GetAxis("Horizontal");
        float moveVertical = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);

        rb.AddForce(movement * speed);
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Cible"))
        {
            other.gameObject.SetActive(false);
            count = count + 1;
            SetCountText();
        }
    }
    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Danger"))
        {

            nbreVies = nbreVies - 1;
            SetCountVies();


        }
        if (collision.gameObject.CompareTag("Corona"))
        {

            if (count >= 6)
            {
                collision.gameObject.SetActive(false);
                winText.text = "Vous êtes toujours sain, Continuez!";

            }
            else
            {
                winText.text = "Vous avez besoin d'un score égale à 6";
            }
        }
    }

    void SetCountText()
    {
        countText.text = "Score: " + count.ToString();
        if (count >= 8 && nbreVies >= 0)
        {
            winText.text = "You Win!";
        }
    }
    void SetCountVies()
    {

        countVies.text = "Vies : " + nbreVies.ToString();
        if (nbreVies == 0)
        {
            
            countText.text = "";
            Time.timeScale = 0;
            //Application.LoadLevel(Application.loadedLevel);
            winText.text = "Game Over !! Vous n'avez plus de vie!!";
        }
    }

   
}

