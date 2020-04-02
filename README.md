# alexa-prep-me
Interview with Alexa!

## How to get started?
Since this app has not been published into the market place, if you would like to install it on your Alexa devices, go to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) and click on **Create a Skill** and click on **Custom** and Choose **Start from scratch**.

![alt text](https://github.com/kmorawala/Alexa-Interview-Me/blob/master/Images/Create_Skill.png "Create a Skill")

### Build Tab
Give an appropriate **invocation** word under **Skill Invocation Name** field for your app. This word will start the skill when uttered by the user.


Under **Intents**, use the files from **Skill Invocation Name** folder to name and import various **Utterances**.

Similarly, use **Categories-values-slots.csv** file to create custom slot values.

Finally, click on **Save Model** and then **Build Model**. This step needs to be performed every time a change on the **Build** tab is made.

### Code Tab

Upload all of the remaining files to this tab, unless any of these files already exist and look identical. All the .txt files represent various categories of coding questions, one per line of the file. Further, the categories would match up to the slot values of **Categories** under the Build tab.

Click on **Save** first. Once successfully saved, click on **Deploy**. This step may require additional configuration on AWS lambda when doing it for the first time. Every time something under the **Build** tab changes, these steps have to be performed.

### Test Tab
This is where you can type in or speak to test your app on the left side and you will see JSON response on the right side.

If you reached this point, you have successfully made a wonderful app on your Alexa device. Test it out now! Be sure that you are using the same amazon account for your device as well as for the developer console.

Feel free to edit the app on your console and contact me if you have any questions/share your feedback with me!
