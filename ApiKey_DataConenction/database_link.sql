-- ==============================================================================
 Database-to-Database Linking (Pure SQL)
-- Goal: Query and join data across two completely separate database architectures
-- ==============================================================================

-- 1. LINK THE REMOTE DATABASE SYSTEM
-- In SQL Server, this is: EXEC sp_addlinkedserver @server='RemoteFinanceDB'
-- In PostgreSQL, this is: CREATE FOREIGN DATA WRAPPER ...
-- In SQLite, we attach the second database file and give it an alias name:
ATTACH DATABASE 'inventory_system.db' AS RemoteInventoryDB;


-- 2. CREATE A MOCK PRODUCTION TABLE IN THE REMOTE DATABASE
-- This simulates an entirely different system (e.g., an inventory or sales database)
CREATE TABLE IF NOT EXISTS RemoteInventoryDB.product_catalog (
    sku_id INTEGER PRIMARY KEY,
    product_name TEXT,
    stock_count INTEGER
);


-- 3. POPULATE MOCK PRODUCTION DATA 
INSERT OR REPLACE INTO RemoteInventoryDB.product_catalog (sku_id, product_name, stock_count) VALUES
(1, 'Cloud Data Server Rack v2', 45),
(2, 'Developer Multi-Agent Workstation', 12),
(3, 'Enterprise Secure Router', 88);


-- 4. THE INTERVIEW "GOLDEN QUERY": Cross-Database Joining
-- We will join our main staging table (from Scenario 2) with this newly linked remote table.
-- We map them using the explicit database alias prefix.

SELECT 
    staging.id AS PostID,
    staging.title AS API_Post_Title,
    remote.product_name AS Linked_Product,
    remote.stock_count AS Current_Warehouse_Stock
FROM main.staging_posts AS staging
INNER JOIN RemoteInventoryDB.product_catalog AS remote
    ON staging.id = remote.sku_id;


-- 5. CLEAN UP THE LINK
-- Once the migration or query is complete, always detach/drop the connection link
DETACH DATABASE RemoteInventoryDB;