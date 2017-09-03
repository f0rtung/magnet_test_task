import sqlite3


class SQLiteWrapper:
    def __init__(self, db_file_path, init_script=None):
        self.db_file = db_file_path
        if init_script is not None:
            self.__execute_script(init_script)

    def __execute(self, callback, need_commit=True):
        result = None
        try:
            db_connect = sqlite3.connect(self.db_file)
            cursor = db_connect.cursor()
            query_result = callback(cursor)
            if query_result is not None:
                result = query_result.fetchall()
        except sqlite3.DatabaseError as err:
            print(err)
        else:
            if need_commit:
                db_connect.commit()
            db_connect.close()
        return result

    def __execute_script(self, init_script_content):
        def callback(cursor):
            cursor.executescript(init_script_content)

        self.__execute(callback)

    def select_query(self, query, params=()):
        def callback(cursor):
            return cursor.execute(query, params)

        return self.__execute(callback, False)

    def commited_query(self, query, params):
        def callback(cursor):
            return cursor.execute(query, params)

        return self.__execute(callback)

    def insert_query(self, query, params):
        return self.commited_query(query, params)

    def delete_query(self, query, params):
        return self.commited_query(query, params)

    def get_all_regions(self):
        return self.select_query("SELECT * FROM Regions")

    def get_all_cities(self):
        return self.select_query("SELECT * FROM Cities")

    def get_all_cities_by_region_id(self, region_id):
        return self.select_query(
            "SELECT * FROM Cities "
            "WHERE CityID IN "
            "(SELECT CityID FROM RegionCityRelations "
            "WHERE RegionID = ?)", (region_id,)
        )

    def remove_comment(self, comment_id):
        self.delete_query(
            "DELETE FROM CommentInfo "
            "WHERE CommentID = ?",
            (comment_id,)
        )

    def insert_comment(self, comment_data):
        f_name = comment_data["fName"]
        s_name = comment_data["sName"]
        m_name = comment_data.get("mName", "")
        region_id = int(comment_data["region"])
        city_id = int(comment_data["city"])
        email = comment_data["email"]
        phone = comment_data["phone"]
        comment = comment_data["comment"]
        region_city_relation_id = self.get_region_city_relation_id(region_id, city_id)[0][0]
        self.insert_query(
            "INSERT INTO CommentInfo "
            "(LastName, FirstName, MiddleName, RCRelation, Phone, Email, Comment) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            (s_name, f_name, m_name, region_city_relation_id, phone, email, comment)
        )

    def get_region_city_relation_id(self, region_id, city_id):
        return self.select_query(
            "SELECT RelationID "
            "FROM RegionCityRelations "
            "WHERE RegionID = ? AND CityID = ?",
            (region_id, city_id)
        )

    def get_all_comments(self):
        return self.select_query(
            "SELECT LastName, FirstName, MiddleName, "
            "Regions.RegionName, Cities.CityName, Email, Phone, Comment, CommentID "
            "FROM CommentInfo comInf "
            "JOIN RegionCityRelations rcRel ON comInf.RCRelation = rcRel.RelationID "
            "JOIN Regions ON rcRel.RegionID = Regions.RegionID "
            "JOIN Cities ON rcRel.CityID = Cities.CityID"
        )

    def get_region_where_comments_more_than(self, comm_count):
        return self.select_query(
            "SELECT Regions.RegionID, Regions.RegionName, count(CommentID) as commCount "
            "FROM CommentInfo comInf "
            "JOIN RegionCityRelations rcRel ON comInf.RCRelation = rcRel.RelationID "
            "JOIN Regions ON rcRel.RegionID = Regions.RegionID "
            "GROUP BY Regions.RegionID "
            "HAVING commCount > ?",
            (comm_count,)
        )

    def get_cities_stat_by_region_id(self, region_id):
        return self.select_query(
            "SELECT Cities.CityName, count(CommentID) as commCount "
            "FROM CommentInfo comInf "
            "JOIN RegionCityRelations rcRel ON comInf.RCRelation = rcRel.RelationID "
            "JOIN Cities ON rcRel.CityID = Cities.CityID "
            "JOIN Regions ON rcRel.RegionID = Regions.RegionID "
            "GROUP BY Cities.CityID "
            "HAVING Regions.RegionID = ?",
            (region_id,)
        )
