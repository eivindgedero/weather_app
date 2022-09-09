import discord
import requests
from discord.ext import commands
from discord import Embed
import config
from wind_converter import wind_converter


base_url = "https://api.openweathermap.org/data/2.5/weather?"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event 
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def weather(ctx, *, city: str):
    if ctx.channel.id != 784215570173657118:
      await ctx.channel.send("Please use <#784215570173657118>.")
    else:
      unit = "units=metric"
      complete_url = f"{base_url}appid={config.weather_api}&q={city}&{unit}"
      response = requests.get(complete_url)
      result = response.json()

      channel = ctx.message.channel
      if result["cod"] != "404":
          city = result["name"]
          weather_description = result["weather"][0]["description"]
          temperature = result["main"]["temp"]
          minimum_temperature = result["main"]["temp_min"]
          maximum_temperature = result["main"]["temp_max"]
          pressure = result["main"]["pressure"]
          humidity = result["main"]["humidity"]
          wind_speed = result["wind"]["speed"]
          wind_direction = result["wind"]["deg"]
          print(wind_direction)
          embed=discord.Embed(title=f"{city}", color=0x14aaeb)
          embed.add_field(name="Temperature", value=f"{temperature}°C", inline = True)
          embed.add_field(name="max", value=f"{maximum_temperature}°C", inline = True)
          embed.add_field(name="min", value=f"{minimum_temperature}°C", inline = True)
          embed.add_field(name="Description", value=f"{weather_description}", inline = False)
          embed.add_field(name="Wind condition", value=f"{wind_speed}m/s {wind_converter(wind_direction)}", inline = False)
          embed.add_field(name="Pressure", value=f"{pressure}hPa", inline = True)
          embed.add_field(name="humidity", value=f"{humidity}%", inline = True)          
          await channel.send(embed=embed)
      else:
          await channel.send("City not found.")
          
bot.run(config.secret)