from mcp.server.fastmcp import FastMCP
import mysql.connector
import os

mcp = FastMCP(name="inventory_mcp")

# MySQL database configuration
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Ritesh@Bhadana20"),
    "database": os.getenv("DB_NAME", "ritesh_inventory")
}


@mcp.tool()
def add_inventory(item_id: str, product_name: str, location: str, quantity: int) -> dict:
    """Add or update inventory item. If item exists, increases quantity."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventory (item_id, product_name, location, quantity) VALUES (%s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE quantity = quantity + %s, product_name = VALUES(product_name)",
            (item_id, product_name, location, quantity, quantity)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": f"Added {quantity} units of {product_name} ({item_id}) at {location}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def remove_inventory(item_id: str, location: str, quantity: int) -> dict:
    """Remove quantity from inventory. Only removes if sufficient stock exists."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = quantity - %s WHERE item_id=%s AND location=%s AND quantity >= %s",
            (quantity, item_id, location, quantity)
        )
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        
        if rows_affected > 0:
            return {"status": "success", "message": f"Removed {quantity} units of {item_id} from {location}"}
        else:
            return {"status": "error", "message": f"Insufficient stock or item not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def check_stock(item_id: str, location: str) -> dict:
    """Check stock level for a specific item at a location."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT product_name, quantity FROM inventory WHERE item_id=%s AND location=%s",
            (item_id, location)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return {
                "status": "success",
                "item_id": item_id,
                "location": location,
                "product_name": result[0],
                "quantity": result[1]
            }
        else:
            return {
                "status": "not_found",
                "item_id": item_id,
                "location": location,
                "product_name": None,
                "quantity": 0,
                "message": "Item not found at this location"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def list_inventory(location: str = None) -> dict:
    """List all inventory items. Optionally filter by location."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        if location:
            cursor.execute(
                "SELECT item_id, product_name, location, quantity FROM inventory WHERE location=%s ORDER BY product_name",
                (location,)
            )
        else:
            cursor.execute("SELECT item_id, product_name, location, quantity FROM inventory ORDER BY product_name")
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"status": "success", "count": len(rows), "items": rows}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def get_total_stock(item_id: str) -> dict:
    """Get total stock across all locations for a specific item."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT location, quantity FROM inventory WHERE item_id=%s",
            (item_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if rows:
            total = sum(row['quantity'] for row in rows)
            return {
                "status": "success",
                "item_id": item_id,
                "total_quantity": total,
                "locations": rows
            }
        else:
            return {
                "status": "not_found",
                "item_id": item_id,
                "message": "Item not found in any location"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    mcp.run()