using System.Collections;
using UnityEngine.UI;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Timer : MonoBehaviour
{
    
    public float timeLeft = 30.0f;
    public Text timerText; 


    void Update()
    {
        timeLeft -= Time.deltaTime;
        timerText.text = "Secondes restantes : "+(timeLeft).ToString("0");
        if (timeLeft < 0)
        {
          
            Time.timeScale = 0;
            //Application.LoadLevel(Application.loadedLevel);
            
        }
       
    }
}
