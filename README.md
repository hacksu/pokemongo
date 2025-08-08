# mongodb-lesson

So as we all know, normally when we write and run a program all of the variables and objects and whatnot we've created evaporate as soon as it finishes, and the next time we run that program it's completely back to square one. Obviously that's not how programs in the "real world" tend to work; they store information persistently; and one way they do that is by using databases to store a program's thoughts and ideas. A database is a program that runs alongside our program; it will receive stuff from our program, hold on to it even when our program's not running, and store it in some files somewhere in a very efficiently readable format so it's kept \*permanently\*, and we still have it, even if we turn our computer off, or lose power during a once-in-a-century thunderstorm.

There's a language for giving commands to databases called SQL. We won't be using it, but it was really popular for some time, and some people claim they can still hear its voice. Instead we'll be using a NoSQL database; the technical definition of the term NoSQL is, it's a database that doesn't use SQL. [MongoDB is the most popular NoSQL database.](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-databases) It stores data in documents. Documents have other names in other contexts, like "dicts" in pure Python and "objects" in JavaScript, but I'm just going to call them documents here; you will become extremely tired of the word. Documents look like this:

### Document example: data for a person

```Python
{
  "name": "Mitch",
  "balance": -10.17,
  "happy": False,
  "brain_cells_gone_forever": 10245
}
```

So you can kind of see what's going on here; on the left are labels, usually called "keys" for some reason, and on the right are values that match those labels. In documents like this, the data is kind of the important part and the keys or labels are just ways to name them so you can retrieve them later. This pattern of storing data entries with labels that indicate their meaning is a common one in programming. In fact, you could say that whenever you make a variable in a programming language, you're storing a data entry with a label - the variable name - attached. In the context of a database, though, things are a little different; we're going to want to go one step further and store multiple documents like this, each with a different attached to these labels, like for this example each document would have a different value for "name"; MongoDB is set up to store collections of documents, meaning for this example, information on a whole bunch of students, and we're going to be exploring one obvious use case for a database full of documents like this.

**REFERENCE BUILD INSTRUCTIONS**<br>
For simple interaction we've put together a custom Docker Image that will prepare the MongoDB on your system, the python code we will be reviewing shortly will try to connect to a mongodb service running locally. We supply instructions on building this [HERE](BUILD.md)

So I've set up a database containing a document for each species of the first seven generations of Pokemon, and this is how we're going to connect to it.

Note: now that the lesson is over, you will have to set up a database yourself. It isn't difficult; you can just [download](https://www.mongodb.com/try/download/community) the program here and run it on your own computer, or [make a free account](https://www.mongodb.com/try) and get access to a database in the cloud. Then, connect to the database with MongoDBCompass or write your own program and import the file "pokemon_data/pokedex.json" in a collection called pokedex in a database called pokemon, and also create an empty collection called "PC" for later.

```python
from pprint import pprint  # not a mongodb thing, but useful for displaying documents
from pymongo import MongoClient

client = MongoClient("your config")
database = client.pokemon  # get the database called "pokemon" on this server
collection = database.pokedex  # get the collection called "pokedex" in that database
```

And this is how you retrieve the document corresponding to a Pokemon and print it:

```python
pikachu = collection.find_one({"name": "Pikachu"})
pprint(pikachu)
```

So. Do you all see Pikachu?

You've just retrieved a MongoDB document, and it's giving you information about a Pokemon. If you want information about some other Pokemon, feel free to replace "Pikachu" with its name. The data, the variables that we retrieved are inside the document, but we can get them out pretty easily. If you want to see Pikachu's base HP, just do this:

```
print(pikachu["HP"])
```

So in MongoDB, you create queries by creating sort of mini-documents that specify what you're looking for, like the one we have here. This was a really really simple one: we had one key and one value; that pair had to be present in a document in the database for it to match. But we can do more subtle things as well; for example, instead of looking for a `"name"` that is `"Pikachu"`, we could look for a `"HP"` that is `greater than 120`. So the first part of requesting that looks pretty familiar:

```python3
good_hp = collection.find_one({"HP":           })
```

But to specify the exact condition we're looking for, we're going to need to express the concept "greater than" and the number "120". We can do that by making another mini-document, with that first thing as the key and the second thing as the value:

```python
good_hp = collection.find_one({ "HP": {"$gt": 120} })
```

So this introduces us to the wonderful world of operators.

Did that work for everyone? It's okay that only one result showed up.

Operators are special key that start with dollar signs that have a special meaning within MongoDB. Something interesting is that when we're looking at a document, the values are what is important and the keys were just labels for the values, but when dealing with operators, you have to see the key and the value as both conveying information; basically, whenever an operator is used as a key, it's telling MongoDB what to do with a certain value. In this case, it's telling it to use this value in a greater-than comparison. This is just one example of a comparison operator, so-called because it compared a thing to something. There are quite a few comparison operators, and we're not going to test out all of them, but they follow pretty much what you'd expect, if you just think about comparing one thing to another: there's $gte (greater than or equal to), $lt (less than), and even $ne (not equal to), and the other usual suspects from conditional statements.

![](helpful_stuff/comparison-operators.png)

By the way, we're only getting one Pokemon at a time because we're using `find_one`. To get more, you can just use `find`, but that returns a thing called a cursor which you can go study if you want but we're going to want to turn it into a list to easily read the results. Like this:

```python
bad_hp = list(collection.find({ "HP": {"$lt": 15} }))
```

So yeah, to get multiple Pokemon, you just switch `find_one` to `find`, and then wrap the whole thing in list().

We just learned about operators that act on individual values. There is actually another type of operator that takes in entire queries of the type we've just been using. One pretty normal one is called "$or". If you want to get documents that match this query OR that query, you take both of them, put them in a list by going `[query1, query2]`, and make that list the value in a document with the key "$or":

```python
multiple_queries = [
    { "HP": {"$gt": 220}},
    {"Defence": {"$gt": 220}}
]
good_hp_or_good_defence = list(collection.find({ "$or": multiple_queries }))
pprint(good_hp_or_good_defence)
```

That might look kind of alien and complicated, but we can break it down. These two initial queries, we know about those: one sets a criterion for the value that corresponds to HP in the Pokemon documents, and one sets a criterion for the Defense, which we haven't used in a query before but we've seen it in our printed results. Those are both in a list. Because the list is there as the value for the "$or" operator, we get back documents where the first thing matches OR the second thing matches. And so here are our results. As you might expect, there are other logical operators than $or, that work pretty much exactly the same way. Like these:

![](helpful_stuff/logical-operators.png)

Anyway, querying even with a simple document can be surprisingly deep. You may have noticed that all these pokemon have a list of types attached to them, because pokemon can have more than one type. mongodb makes it really easy to deal with lists of data: you can query for any pokemon that are flying type like this. you're just specifying a single value, "Flying", in the query, but MongoDB will search through the lists of types that every pokemon has to find matches for it.

```python
pprint(collection.find_one({"type": "Flying"}))
```

And, or course, I don't know if you guys have been noticing this, but there are documents Inside Our Documents! Inside the normal Pokemon data, there is a sub-document that indicates what the stats of a Pokemon are with regard to special moves. There is no limit in MongoDB to putting lists in documents, or documents in documents, or documents in lists in lists in documents. All the data can nest freely. This is the big thing that makes it so powerful compared to old SQL databases, which were entirely based on tables where every database entry had to fit into a row that had a specific number of specific values of certain types. In MongoDB it's the wild west. But our example is not too crazy. But you are wondering, I'm very confident, how you would retrieve a document based on the number it has for special attack.

It's also not too difficult. You just compose a path by taking the key that points to the inner document and then putting a dot and then putting the key in the inner document that you were worried about, and then use that path just like a normal key. If you had many layers of document, you would have thing dot thing dot thing dot thing. But our case is downright sane.

```python
pprint(collection.find_one({"Special.Attack": 109}))
```

Those are the basics of querying. There are a couple of other small topics we could dive into; we could learn how to limit the exact number of documents we retrieve at one time, or a few more ways to probe into arrays in document, but we've covered the fundamental building blocks of what you do. The rest is details.

And now I'm going to ask you to make a new file; for this one, you're going to learn how to insert.

The initial connection is the same, but you're going to connect to a different collection from this time. You're going to connect to the PC, a collection that you have permission to write to, where individual Pokemon are stored:

```python
from pprint import pprint
from pymongo import MongoClient

client = MongoClient("your config")
db = client.pokemon
collection = db.PC
```

And the code for inserting is actually really simple. Don't do it yet.

```python
collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "hp": 100,   # important
  "xp": 0,    # important
  "mood": "bemused"
})
```

So that's the basic idea; that's how you take data and store it somewhere where it will persist outside of your program. We're going to add one thing, though. MongoDB assigns a unique ID to every document that's inserted, and we're going to print the unique ID of our documents like this:

```python
collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "hp": 100,   # important
  "xp": 0,    # important
  "mood": "bemused"
})
print(result.inserted_id)
```

You can follow the format that I have for my Pokemon here if you want, but you can also put any strings for keys and pretty much any values that aren't objects. Here I have MongoDB Compass, which is a great program that lets you monitor a MongoDB database, and we can see what you're inserting here. Or if no one wants to insert anything I will just stare forlornly at this empty screen.

And finally, it would be dumb if you could insert a document but then could never modify it once it was there. We need to be able to update the stored information about our Pokemon, or else we would never be able to do anything Pokemonish with them. We'll want to make yet another new file for updating, so we're not re-running our inserts and making a new document every time we want to update; but we want to copy the ID we got from running an insert, because that's how you are going to identify the Pokemon you're going to modify.

An update consists of two parts: one query to identify the document that will be modified, and one mini-document specifying the action to be taken. For the query, we're going to use your pokemon's ID, which we printed out when we inserted it. When we printed it, we saw it as a string, but technically, to make life more difficult, it's an object of a class called, inspiredly, ObjectId. If you're not into classes and objects, don't worry about it, that just means we have to import the ObjectId constructor and call it with our ID string before using it. Like this:

```python
from bson.objectid import ObjectId
my_id = ObjectId("whatever")
```

and again, to make life more difficult, instead of this important ID being labeled "id", it's labeled "\_id". So our query will need to look like this:

```python
id_query = { "_id": my_id }
```

In addition to the querying operators we looked at before, there are update operators. We're going to stick with a simple one here: $set. $set just lets you list new data that you want to add to your document, overriding old data if it exists. So, finally, our update operation looks like this:

```python
collection.update_one(
    id_query,
    {"$set": {"owner": "Mitch"}}
)
```

So yeah. We're updating with one query that indicates which document to update and one update operator that says what to do to it. Update operators are interesting because some of them let you modify data without even knowing what it is or what you're changing it into. So you might not know what your pokemon's current health is, but let's say you want to increase it by 5. You can do that while continuing not to know what it is by just telling MongoDB with the $inc (increment) operator that that's what it should do:

```python
pprint(collection.fetch_one(id_query))
print("incrementing health...")
collection.update_one(
  id_query,
  { "$inc": {"hp": 5} }
)
pprint(collection.fetch_one(id_query))
```

So instead of $set, we're using $inc, which stands for increment, and instead of saying what we want the health to be set to, we're just saying how much we want it to be incremented by. In this case 5. The other update operators let you do things like multiplying a value by a number, changing it to be at least a given number, adding a thing to an array, and stuff like that.

So that shows us how to retrieve, store, and update documents in MongoDB. At this point, you might be interested to know that you can download MongoDB Community Edition and connect to a database running on your very own computer, to use it for persistent data in any program you may write. This example is in Python, but you can connect to it in a very similar way with its official libraries for JavaScript, Java, C++, and even Rust, and some other ones. This is a very popular software among new developers, so there are a ton of tutorials online for lots of different languages that can help you set up or learn more on your own.

Anyway, that's enough boring stuff about databases. Let's move on to game design. I had an idea for a really simple Pokemon game we could program. Basically, you would have your own personal Pokemon, and then you would get a random one, from.... somewhere. And then you could choose to either fight or flee from the random Pokemon. If you fought it, your HP would go down a little but your XP would go up. If you fled from it, the other Pokemon's XP would go up for very efficiently winning the encounter. And the goal would be to have your Pokemon be the first to reach some XP value, like 100. So I haven't tested, or thought about this game very hard at all, and it probably will be a disaster. But, it would be an accomplishment to program it. The only hard part is, where would we get the Pokemon to battle against, and how could we store the store the HP and XP of all the different Pokemon in a persistent and reliably accessible manner?

Wait. Okay.

So, I think we can create this program. First, let's take all the connection and import stuff from our update file, including our ID query. Second, let's retrieve our pokemon and print them to see what they look like at the moment.

This is the part where I explain the code in example_code/game.py.

The interesting thing about this program is that normally, if you want to do something over and over again in a loop and continuously update some piece of data the whole time, you have to actually write a loop with variables that keep track of the data. With this program, instead, you're relying on the database to keep track of the data persistently and every time you run the program you have the same pokemon that you did when it previously finished running. So that's the magic of databases. Maybe you actually wouldn't want to design a game like this, where you had to restart every time you did something. So let's say that this section wasn't about game design actually and was about databases after all.
