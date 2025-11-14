from typing import Any, List, Set


# 1. Generic Unweighted Directed Graph Data Structure
class UnweightedDirectedGraph:
    """
    A generic unweighted directed graph data structure.
    Uses adjacency list representation for efficient edge operations.
    """

    def __init__(self):
        # Dictionary where key: vertex, value: set of outgoing adjacent vertices
        self.adjacency_list = {}

    def add_vertex(self, vertex: Any) -> None:
        """Add a new vertex to the graph if it doesn't exist"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = set()

    def add_edge(self, from_vertex: Any, to_vertex: Any) -> None:
        """
        Connect one vertex with another vertex (directed edge)
        from_vertex -> to_vertex
        """
        if from_vertex not in self.adjacency_list:
            self.add_vertex(from_vertex)
        if to_vertex not in self.adjacency_list:
            self.add_vertex(to_vertex)

        self.adjacency_list[from_vertex].add(to_vertex)

    def list_outgoing_adjacent_vertex(self, vertex: Any) -> List[Any]:
        """List all vertices where edges are outgoing from the given vertex"""
        if vertex not in self.adjacency_list:
            return []
        return list(self.adjacency_list[vertex])

    def list_incoming_adjacent_vertex(self, vertex: Any) -> List[Any]:
        """List all vertices that have outgoing edges to the given vertex (followers)"""
        followers = []
        for v, neighbors in self.adjacency_list.items():
            if vertex in neighbors:
                followers.append(v)
        return followers

    def get_all_vertices(self) -> List[Any]:
        """Get all vertices in the graph"""
        return list(self.adjacency_list.keys())

    def remove_edge(self, from_vertex: Any, to_vertex: Any) -> bool:
        """Remove an edge between two vertices"""
        if from_vertex in self.adjacency_list and to_vertex in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].remove(to_vertex)
            return True
        return False

    def has_vertex(self, vertex: Any) -> bool:
        """Check if vertex exists in graph"""
        return vertex in self.adjacency_list


# 2. Person Entity Class
class Person:
    """
    Represents a single user of a social media app.
    Follows domain-driven design principles.
    """

    def __init__(self, name: str, gender: str, biography: str, is_private: bool = False):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.is_private = is_private
        self.join_date = "2024"  # Simplified join date

    def get_name(self) -> str:
        return self.name

    def get_gender(self) -> str:
        return self.gender

    def get_biography(self) -> str:
        return self.biography

    def get_privacy_status(self) -> str:
        return "Private" if self.is_private else "Public"

    def is_profile_private(self) -> bool:
        return self.is_private

    def __str__(self) -> str:
        """String representation for display"""
        privacy_status = "Private" if self.is_private else "Public"
        return f"Name: {self.name}\nGender: {self.gender}\nBio: {self.biography}\nProfile: {privacy_status}\nJoined: {self.join_date}"

    def __hash__(self) -> int:
        """Make Person object hashable for use in graph vertices"""
        return hash(self.name)

    def __eq__(self, other) -> bool:
        """Equality comparison for graph operations"""
        if not isinstance(other, Person):
            return False
        return self.name == other.name


# 3. Social Media App Controller
class SocialMediaApp:
    """
    Controller class that uses the generic graph to implement social media functionality.
    Demonstrates separation of concerns and abstraction.
    """

    def __init__(self):
        self.graph = UnweightedDirectedGraph()
        self.people = []
        self.initialize_sample_data()

    def initialize_sample_data(self):
        """Create sample user profiles and follow relationships"""
        # Create person profiles (5-10 people as required)
        sample_people = [
            Person("Alice Johnson", "Female", "Software engineer and dog lover", False),
            Person("Bob Smith", "Male", "Travel enthusiast and photographer", False),
            Person("Charlie Brown", "Male", "University student studying AI", True),
            Person("Diana Prince", "Female", "Professional athlete and coach", False),
            Person("Ethan Hunt", "Male", "Adventure seeker and movie buff", True),
            Person("Fiona Gallagher", "Female", "Artist and mural painter", False),
            Person("George Miller", "Male", "Chef and food blogger", False)
        ]

        # Add people to graph and store references
        for person in sample_people:
            self.add_person(person)

        # Create follow relationships (mimicking Instagram-style connections)
        self.create_follow_relationships()

    def add_person(self, person: Person) -> None:
        """Add a person to the social network"""
        self.graph.add_vertex(person)
        self.people.append(person)

    def create_follow_relationships(self):
        """Create realistic social media follow relationships"""
        people = self.people

        # Alice follows Bob and Diana
        self.graph.add_edge(people[0], people[1])  # Alice -> Bob
        self.graph.add_edge(people[0], people[3])  # Alice -> Diana

        # Bob follows Alice, Charlie, and Fiona
        self.graph.add_edge(people[1], people[0])  # Bob -> Alice
        self.graph.add_edge(people[1], people[2])  # Bob -> Charlie
        self.graph.add_edge(people[1], people[5])  # Bob -> Fiona

        # Charlie follows Diana and Ethan
        self.graph.add_edge(people[2], people[3])  # Charlie -> Diana
        self.graph.add_edge(people[2], people[4])  # Charlie -> Ethan

        # Diana follows Alice and Fiona
        self.graph.add_edge(people[3], people[0])  # Diana -> Alice
        self.graph.add_edge(people[3], people[5])  # Diana -> Fiona

        # Ethan follows Bob and George
        self.graph.add_edge(people[4], people[1])  # Ethan -> Bob
        self.graph.add_edge(people[4], people[6])  # Ethan -> George

        # Fiona follows Charlie and Diana
        self.graph.add_edge(people[5], people[2])  # Fiona -> Charlie
        self.graph.add_edge(people[5], people[3])  # Fiona -> Diana

        # George follows Alice and Ethan
        self.graph.add_edge(people[6], people[0])  # George -> Alice
        self.graph.add_edge(people[6], people[4])  # George -> Ethan

    def display_all_users(self) -> None:
        """Display a list of all users' names"""
        print("\n" + "=" * 40)
        print("          ALL USERS")
        print("=" * 40)
        for i, person in enumerate(self.people, 1):
            privacy_icon = "🔒" if person.is_private else "🌐"
            print(f"{i}. {person.name} {privacy_icon}")

    def view_profile_details(self, index: int) -> None:
        """View the profile of any one person in detail"""
        if 1 <= index <= len(self.people):
            person = self.people[index - 1]
            print("\n" + "=" * 40)
            print(f"        PROFILE: {person.name}")
            print("=" * 40)
            print(person)

            # Show follow statistics
            following = self.graph.list_outgoing_adjacent_vertex(person)
            followers = self.graph.list_incoming_adjacent_vertex(person)

            print(f"\nFollow Stats:")
            print(f"Following: {len(following)} users")
            print(f"Followers: {len(followers)} users")
        else:
            print("Invalid user selection!")

    def view_followed_accounts(self, index: int) -> None:
        """View the list of followed accounts of a particular person"""
        if 1 <= index <= len(self.people):
            person = self.people[index - 1]
            following = self.graph.list_outgoing_adjacent_vertex(person)

            print(f"\n{person.name} is following {len(following)} users:")
            print("-" * 30)

            if not following:
                print("Not following anyone yet.")
            else:
                for i, followed_person in enumerate(following, 1):
                    privacy_icon = "🔒" if followed_person.is_private else "🌐"
                    print(f"{i}. {followed_person.name} {privacy_icon}")
        else:
            print("Invalid user selection!")

    def view_followers(self, index: int) -> None:
        """View the list of followers of a particular person"""
        if 1 <= index <= len(self.people):
            person = self.people[index - 1]
            followers = self.graph.list_incoming_adjacent_vertex(person)

            print(f"\n{person.name} has {len(followers)} followers:")
            print("-" * 30)

            if not followers:
                print("No followers yet.")
            else:
                for i, follower in enumerate(followers, 1):
                    privacy_icon = "🔒" if follower.is_private else "🌐"
                    print(f"{i}. {follower.name} {privacy_icon}")
        else:
            print("Invalid user selection!")

    def get_user_selection(self) -> int:
        """Helper method to get user selection with validation"""
        try:
            return int(input("\nSelect user (1-{}): ".format(len(self.people))))
        except ValueError:
            return -1


# 4. Menu-Driven Program
def main():
    """Main menu-driven program for the social media app"""
    app = SocialMediaApp()

    while True:
        print("\n" + "=" * 50)
        print("       SOCIAL MEDIA APP - GRAPH SYSTEM")
        print("=" * 50)
        print("1. Display all users' names")
        print("2. View profile details of any user")
        print("3. View followed accounts of a user")
        print("4. View followers of a user")
        print("5. Display graph statistics")
        print("6. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            app.display_all_users()

        elif choice == '2':
            app.display_all_users()
            selection = app.get_user_selection()
            if selection != -1:
                app.view_profile_details(selection)

        elif choice == '3':
            app.display_all_users()
            selection = app.get_user_selection()
            if selection != -1:
                app.view_followed_accounts(selection)

        elif choice == '4':
            app.display_all_users()
            selection = app.get_user_selection()
            if selection != -1:
                app.view_followers(selection)

        elif choice == '5':
            display_graph_statistics(app)

        elif choice == '6':
            print("Thank you for using the Social Media Graph System!")
            break

        else:
            print("Invalid choice! Please enter a number between 1-6.")

        input("\nPress Enter to continue...")


def display_graph_statistics(app: SocialMediaApp):
    """Display graph statistics and structure"""
    print("\n" + "=" * 40)
    print("        GRAPH STATISTICS")
    print("=" * 40)

    total_vertices = len(app.graph.get_all_vertices())
    total_edges = sum(len(neighbors) for neighbors in app.graph.adjacency_list.values())

    print(f"Total Users (Vertices): {total_vertices}")
    print(f"Total Follows (Edges): {total_edges}")
    print(f"Average Follows per User: {total_edges / total_vertices:.2f}")

    # Find most followed user
    max_followers = 0
    popular_user = None
    for person in app.people:
        followers = len(app.graph.list_incoming_adjacent_vertex(person))
        if followers > max_followers:
            max_followers = followers
            popular_user = person

    if popular_user:
        print(f"Most Popular User: {popular_user.name} ({max_followers} followers)")

    print("\nGraph Structure Preview:")
    print("-" * 30)
    for i, person in enumerate(app.people[:3], 1):  # Show first 3 for preview
        following = app.graph.list_outgoing_adjacent_vertex(person)
        print(f"{person.name} → Following: {[p.name for p in following]}")


# Run the program
if __name__ == "__main__":
    main()